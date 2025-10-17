Title: Understanding Cookies and CSRF with Django
Date: 2025-10-17 15:49
Category: django
Tags: django
Slug: understanding-cookies-and-csrf-with-django
Authors: me
Summary: Clarifying how cookies and CSRF protection work together
PreviewImage: images/blog/cookies.png

--------------------------------------------------------
    
# Understanding Cookies and CSRF in Django

## Intro

Over the past few weeks, as part of our annual SOC II audit, I've been reviewing the security of how authentication workflow. I wrote this article to clarify how some concepts work in our products for the developers on my team, and thought this could be useful to others.

## 1. What Cookies Actually Are

Cookies are small pieces of data that your browser stores for a website. Every time your browser sends a request to that site, it automatically includes any cookies that belong to it.

They’re what let websites “remember” things — like that you’re logged in, what’s in your cart, or what theme you picked.

Each cookie has a few properties that tell the browser how and when to send it, like:

* its name and value,
* which domain and path it applies to,
* how long it lasts,
* and a few security flags like `HttpOnly`, `Secure`, and `SameSite`.

Without cookies, every request would look like it’s coming from a brand-new visitor — which is why they’re so central to authentication.

**One important fact to be clear about:** Cookies are only sent with requests to the **same domain that issued them**. If you log in to `app.mydomain.com`, your browser will only send that cookie back to `app.mydomain.com` — not to any other site. This is the foundation of how browsers isolate data between websites.

When you are on a given website, you can open the dev tools > Storage and see the list of cookies:

![Cookies in Dev Tools](images/blog/cookies-screenshot.png)

## 2. How Django Session Authentication Works

Django’s default way to handle login sessions is called **session authentication**. Here’s how it works, step by step:

1. When a user logs in, Django creates a "session" on the server. Where the session is stored is controlled by the `SESSION_ENGINE` settings, and for our products we use Redis, but it's also possible to store them in the database or in a file.
2. Django gives the browser a cookie (usually called `sessionid`).
3. The cookie doesn’t contain any personal data — just a random session key.
4. On each request to the app domain name, the browser automatically includes that cookie, and Django looks up which user it belongs to.

So when you see `request.user` in Django, that’s the session system doing its work behind the scenes.

The key idea is that the cookie is just a pointer — all the real data stays safely on the server.

## 3. What CSRF Attacks Are (and Why We Care)

Now that we know cookies are sent automatically, let’s talk about a common attack that abuses this: **Cross-Site Request Forgery (CSRF)**.

Imagine this:

1. You’re logged into your app and your browser has your `sessionid` cookie.
2. While still logged in, you visit a shady website called `evil.com`.
3. That site quietly includes a hidden form that submits a POST request to `https://app.mydomain.com/api/delete_account/`.
4. When your browser submits the form, it automatically includes your `sessionid` cookie — because it still belongs to `app.mydomain.com`.
5. From Django’s perspective, it looks like *you* clicked “delete my account.”

That’s a CSRF attack — the attacker “forged” a request using your browser and your valid session cookie.

Without protection, a site could trick your browser into performing any action you’re authorized to do.

## 4. How Django’s CSRF Protection Stops This

Django solves this problem using a **CSRF token** — a secret value that helps verify that every state-changing request truly came from your own site and not from somewhere else.

Let’s revisit the example from above, but this time with Django’s CSRF protection enabled.

### Step-by-Step Example

1. When you log in to `https://app.mydomain.com`, Django sets two cookies:

   * `sessionid`: used to identify your login session.
   * `csrftoken`: a random secret token used for CSRF protection.

2. When Django serves a page that contains a form, it embeds the CSRF token in that page.
   For example, in a Django template, you'll often see:

```html
<form method="POST">
    {% csrf_token %}
    ...
</form>
```

This template tag inserts a hidden input like:

```html
<input type="hidden" name="csrfmiddlewaretoken" value="abc123...">
```

1. When you submit the form, both the cookie and the hidden token are sent back to the server.

   * The browser automatically sends the `csrftoken` cookie.
   * The form submits the hidden token value in the POST body.

2. Django's CSRF middleware checks that the token in the form matches the one in the cookie. If they match, Django knows the request came from a genuine page served by `app.mydomain.com`.

3. Now imagine the malicious site again (`evil.com`).
   It tries to submit the same POST request to `https://app.mydomain.com/api/delete_account/`, but:
    * It cannot read your CSRF cookie (browsers don’t let one site read another site’s cookies).
    * It cannot include the correct CSRF token in the request.


4. As a result, Django sees a missing or invalid token and immediately rejects the request with a `403 Forbidden`.

So even though your browser still sends the `sessionid` cookie automatically, Django’s CSRF middleware stops the request from being accepted — because the secret CSRF token doesn’t match.

### Why This Works So Well

* The CSRF cookie itself is harmless: it doesn’t grant access to anything; it just stores a random value.
* The protection relies on a *double submit* principle: Django expects both a cookie and a matching token from the same origin.
* Since attackers can’t read cookies from another domain, they can’t guess or replay a valid CSRF token.

This small extra step effectively blocks one of the most common web vulnerabilities — all while being invisible to the user.

## 5. How Cookie Attributes Keep Things Safe

Below I break down the common cookie attributes we use and show, for each one, a short example of the kind of attack it helps mitigate.

### HttpOnly

#### What it does

Prevents client-side JavaScript from reading the cookie value.

#### Why we use it

Set `HttpOnly` on cookies that don’t need to be read by JS (for us that’s typically `sessionid`). This reduces the damage if an attacker can run JavaScript on the page (XSS).

#### Attack it mitigates — XSS token theft example

If an attacker finds an XSS hole and injects `<script>` that tries `document.cookie`, any cookie with `HttpOnly` won’t be returned to their script. Without `HttpOnly`, a script could steal `sessionid` and send it to the attacker, allowing session hijacking.

#### Notes

CSRF tokens must be readable by JS when the front-end needs to include them in AJAX requests, so `csrftoken` is often not set to `HttpOnly`.

### Secure

#### What it does

Instructs the browser to send the cookie only over HTTPS connections.

#### Why we use it

Protects cookie values from being exposed over plaintext HTTP, which can be sniffed on the network.

#### Attack it mitigates — network eavesdropping / man-in-the-middle example

If someone is intercepting traffic on a public Wi-Fi, cookies marked `Secure` won’t be sent over plain HTTP requests the attacker can sniff. Without `Secure`, an attacker could capture the cookie and reuse it to impersonate the user.

#### Notes

Always enable `Secure` in production. Combining `Secure` with `SameSite=None` is required by modern browsers for cross-site cookies.

### Path

#### What it does

Limits which URL paths on the domain the browser will include the cookie with.

#### Why we use it

Narrowing the `Path` reduces exposure — for example, an admin session cookie could be scoped to `/admin/`.

#### Attack it mitigates — limited-scope misused cookie example

If an attacker can induce a request to a lower-risk endpoint (e.g., `/public/`), scoping an admin cookie to `/admin/` prevents that request from including the admin cookie. This lowers the chance of accidental exposure and reduces the blast radius if some endpoint is misused.

#### Notes

Be conservative: overly broad `Path` values increase where the cookie is sent; overly narrow ones can break legitimate flows. Use it when you can segment responsibilities by path.

In our current review of the LEAN authentication flow, I found out that we can use the path attribute to make sure that the refresh token is only sent to the `refresh` endpoint and not sent otherwise.

### SameSite

#### What it does

Controls whether the browser includes the cookie on cross-site requests.

#### Why we use it

A key defense against CSRF. It’s the browser-level control that reduces cookies being sent automatically on cross-site requests.

A cross-site request is a http request from one domain to another.

For instance, consider a page hosted on `badguy.com` that includes a form to submit a POST request to `app.mydomain.com`. If SameSite is set to "None", the session and CSRF cookies will be sent along with the request when the form is submitted, which is obviously not good. To prevent this, the default value for the SameSite attribute is "Lax", which would prevent this scenario.

There are 3 possible values for the SameSite attribute (more details here: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie#samesitesamesite-value>):

With `Strict`, the cookies are only sent with requests to the domain that issued them. This is great, except in one scenario: imagine that you are currently logged into our app and you receive an alert email with a link to click on. This is a cross-origin request, so when you click on it, the browser won't include your existing session cookie and the server will redirect you to the login page.

In this scenario, this is a "safe" request (GET) only used for navigation, and that's what the `Lax` value for the SameSite attribute handles: it prevents including the cookies in cross-origin requests **except if they are for top-level navigation.** With `Lax`, normal link navigation will send the cookies, providing a good user experience, but hidden POSTs or background requests from `evil.com` will not send the cookie.

#### Notes

`Lax` is a good balance for `sessionid` — it preserves bookmark/link behavior while blocking many CSRF vectors. `Strict` is safer but can break expected cross-site navigation. `None` allows all cross-site sends and should be avoided unless necessary and secured with `Secure`.

### Expires / Max-Age

#### What it does

Controls how long the cookie lives (session cookie vs persistent cookie).

#### Why we use it

Shorter lifetimes reduce the window of opportunity for attackers if a cookie is leaked; persistent cookies improve UX but increase risk.

#### Attack it mitigates — long-lived stolen cookie example

If a persistent cookie is stolen (e.g., via backup leaks), an attacker can reuse it for as long as it’s valid. By setting reasonable expiry times and using refresh mechanisms server-side (e.g., rotating session keys), we reduce exposure.

#### Notes

For very sensitive sessions, prefer shorter max-age and consider requiring re-authentication for sensitive actions.

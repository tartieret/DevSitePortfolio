Title: Jet Lag Coach
Date: 2025-09-01 00:00
Authors: me
Summary: B2C mobile app that builds personalized plans to beat jet lag
Template: project_detail
save_as: projects/jetlagcoach.html
Technologies:typescript,vuejs,capacitor,revenuecat,netlify,supabase
website: https://www.jetlagcoach.com

### What it is

Jet Lag Coach is a B2C mobile app that helps travellers prevent and recover from jet lag. Based on a trip's origin, destination, and schedule, it generates a personalized, day-by-day plan that tells the user when to seek or avoid light, when to sleep, and when to time habits such as caffeine and melatonin, so their body clock shifts to the new time zone as quickly and comfortably as possible.

The app is aimed at frequent flyers, business travellers, and anyone crossing several time zones who wants a simple, science-based routine to follow before, during, and after a flight, instead of guessing their way through the first few days at a destination.

### How it works

The user enters their travel details and typical sleep pattern, and the app computes a circadian-adjustment schedule tailored to the direction and number of time zones crossed. The plan is presented as a clear timeline with reminders, making it easy to follow each recommended action at the right local time throughout the trip.

### Tech stack

Jet Lag Coach is built as a cross-platform app from a single **TypeScript** and **Vue.js** codebase, packaged for iOS and Android with **Capacitor** so the same web app ships as native mobile builds. Subscriptions and in-app purchases are handled through **RevenueCat**, which manages entitlements and billing across both app stores.

On the backend, the project uses **Supabase** for the database, authentication, and APIs, with the web frontend and serverless functions deployed on **Netlify**. This lightweight, fully managed stack keeps infrastructure overhead low and lets a small team ship and iterate quickly.

### Key features

- Personalized, day-by-day jet lag plans based on trip details
- Light, sleep, caffeine, and melatonin timing recommendations
- Adapts to travel direction and number of time zones crossed
- Cross-platform mobile app (iOS and Android) from one codebase
- Subscription-based access managed with RevenueCat

Title: Avoiding Lost Updates in Web Applications
Date: 2024-12-18 13:49
Category: django
Tags: django,python,webdev
Slug: avoiding-lost-updates-in-web-applications
Authors: me
Summary: Save your future self from sleepless nights and learn to prevent sneaky concurrency bugs
PreviewImage: images/blog/database.jpg

# Avoiding Lost Updates in Web Applications

--------------------------------------------------------

1. [Introduction](#introduction)  
2. [The Problem: Lost Updates with a Django API Endpoint](#problem)  
    2.1 [Demo App](#demo-app)  
    2.2 [Simulating Concurrent Requests](#simulating-concurrent-requests)  
3. [Understanding Read Committed Isolation Level](#understanding)  
    3.1 [What is Read Committed?](#what-is-read-committed)  
    3.2 [What it Doesn't Guarantee](#what-it-doesnt-guarantee)  
4. [Solutions to Avoid Lost Updates](#solutions)  
    4.1 [Solution 1: Atomic Write with `F()` Expressions](#solution1)  
    4.2 [Solution 2: Change Isolation Level to Serializable](#solution2)  
    4.3 [Solution 3: Use `select_for_update()` for Complex Queries](#solution3)  
5. [Conclusion](#conclusion)  
6. [References and Further Readings](#references) 

## <a name="introduction"></a>Introduction

Ignoring concepts like proper database transactions and handling race conditions might seem harmless at first, but it’s a recipe for concurrency bugs that are incredibly hard to debug. These bugs have a knack for showing up at the worst possible time—usually once your app has scaled—leading to massive headaches and sleepless nights. In this post, we’ll explore how to prevent these issues in Django, saving your future self from countless hours of frustration.

Relational databases like PostgreSQL offer various levels of transaction isolation to manage concurrent data access. The most common (and often default settings) is **Read Committed**, which can lead to **lost updates** in certain scenarios. This tutorial demonstrates the problem and explores solutions using a Django application, but the problem and solutions are relevant for any framework.

We'll:

1. Define a basic Django app that increments a counter through an endpoint.
2. Explain the **Read Committed** isolation level and its limitations.
3. Provide solutions:
    1. Using **atomic write operations** with Django's `F` expressions.
    2. Switching to **Serializable** isolation.
    3. Leveraging `select_for_update()` for complex cases.

The demo app and code samples can be found in this repository: <https://github.com/tartieret/django-isolation-levels>

## <a name="problem"></a>1. The Problem: Lost Updates with a Django API Endpoint

### <a name="demo-app"></a>Demo app

Imagine a simple Django app where an endpoint increments a counter stored in a PostgreSQL database. Here's the basic implementation:

```python
# models.py
from django.db import models

class Counter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.PositiveIntegerField(default=0)
```

```python
# views.py
import time

from django.http import JsonResponse
from django.db import transaction

from .models import Counter

@transaction.atomic
def increment_counter(request, name):
    """This endpoint receives a GET request such as:
    GET http://localhost:8000/counters/increment/myCounter/
    """
    # Retrieve the counter object
    counter = Counter.objects.get(name=name)

    # Simulate a slow API endpoint
    time.sleep(5)

    # Increment and save
    counter.value += 1
    counter.save()

    # Return a JSON response
    return JsonResponse({"name": name, "value": counter.value})
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('increment/<str:name>/', views.increment_counter, name='increment_counter'),
]
```

Here, when the `/counters/increment/<name>/` endpoint is called, it retrieves the counter, increments its `value`, and saves the updated value.Simulating Concurrent Requests

Using the admin portal, let's create a first counter called "test," with initial value of zero:

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/3N_vqGmHSjWAMG-image.png)

### <a name="simulating-concurrent-requests"></a>Simulating Concurrent Requests

We'll now try to send multiple requests to this endpoint in parallel, as an example of what could happen in real life with multiple concurrent users.

To simulate concurrent requests, we can use the `concurrent.futures` module in Python to send multiple requests in parallel and build the following `run_test.py` script:

```python
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8000/counters/increment/test/"

# Function to send a request
def send_request(url):
    response = requests.get(url)
    print(response.json())

# Send 10 requests in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(send_request, URL) for _ in range(10)]

print("All requests completed.")
```

The script above will send ten concurrent requests to our local web server. Intuitively, we would expect the final counter value to be equal to 10. Let's run it!

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/eYwVTT6oLsqT4Z-image.png)

What's happening? Each concurrent request returns a value of 1 for the counter!!!

Checking the counter in the admin portal, we can verify that the final value is indeed 1, in spite of having processed ten requests to increment it.

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/huO4fWk7ofQ4x4-image.png)

The schematic below gives a visual representation of what happened:

* The server receives request #1 (in blue), and a zero value is retrieved from the database. It takes a while for the transaction to finish and for the `counter = counter + 1` operation to be committed.
* In the meantime, request #2 (in red) is received and processed similarly. It starts by reading the counter's current value (zero) in the database and incrementing it by one.
* ...
* Similarly, request #n (in green) is received, reads the value of the counter, and commits a new value of `0 + 1 = 1` to the database after about 5 seconds.

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/schema.jpeg)

This problem is known as a **lost update.** Another transaction overwrites changes made by one transaction without the latter being aware of the former's change.

This typically happens when two or more transactions access the same data and then perform an update based on what was read. If there is no locking mechanism in place, we are losing some of the updates as the defaut isolation level (read committed) only guarantees that each transaction is based on a value that was previously committed.

## <a name="understanding"></a>2. Understanding Read Committed Isolation Level

### <a name="what-is-read-committed"></a>What is Read Committed?

Read Committed is the default isolation level in PostgreSQL, Microsoft SQL server, and other relational databases. It ensures that:

* When reading from the database, we only see data that has been committed **(no dirty reads**).
* When writing to the database, we only overwrite data that has been committed (**no dirty writes**)

### <a name="what-it-doesnt-guarantee"></a>What it Doesn't Guarantee

Read Committed **does not prevent non-repeatable reads or lost updates**:

* **Non-repeatable reads**: The same query can return different results within a transaction.
* **Lost updates**: Two transactions can overwrite each other's updates because they operate on the same snapshot of the data.

In our example, all transactions read the same value (`0`), increment it, and overwrite each other's result.

A full description of transaction guarantees and isolation levels is outside the scope of the present article, but I refer you to the following resources for more information:

* PostgreSQL transaction isolation: <https://www.postgresql.org/docs/current/transaction-iso.html>
* Designing Data-Intensive Applications, by Martin Kleppman (Chapter 7): <https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/>

## <a name="solutions"></a> 3. Solutions to Avoid Lost Updates

### <a name="solution1"></a>Solution 1: Atomic Write with `F()` Expressions

The trivial example given above can be avoided by using an atomic update operation, which removes the need to read-modify-write. For example, the counter update can be performed using the following SQL query:

```sql
UPDATE counters SET value = value + 1 WHERE name='test';
```

Django's `F()` Expressions allow you to perform atomic operations at the database level without retrieving and updating the value in Python, which avoids race conditions.

Using this approach, we can add a new endpoint to increment our counter:

```python
# ...
from django.db.models import F
from django.db import transaction


def increment_counter_atomic(request, name):
    with transaction.atomic():
        # Atomically increment the counter
        Counter.objects.filter(name=name).update(value=F('value') + 1)
        counter = Counter.objects.get(name=name)
    return JsonResponse({"name": name, "value": counter.value})
```

Testing again with ten concurrent requests, our counter now increases from 1 to 11, which is what we want:

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/YG7Ic2T0gseUp8-image.png)

This is a simple and efficient solution, but it is limited to simple operations that can be expressed as an atomic update.

### <a name="solution2"></a>Solution 2: Change Isolation Level to Serializable

A more radical option is to modify the Django settings to use a different isolation level, such as **repeatable read** or **serializable**. This can be done for the entire application directly [in the Django settings](https://docs.djangoproject.com/en/5.1/ref/databases/#isolation-level) :

```python
from django.db.backends.postgresql.psycopg_any import IsolationLevel

DATABASES = {
    # ...
    "OPTIONS": {
        "isolation_level": IsolationLevel.SERIALIZABLE,
    },
}
```

The **Serializable** isolation level prevents concurrent transactions from interfering with each other. It ensures that transactions are executed **as if they ran sequentially**.

However, serializable transactions may fail with **serialization errors** if concurrent transactions conflict, requiring retries. Stricter locking can also significantly impact performance.

Alternatively, this can be done for specific raw queries by explicitly setting the isolation level, as shown below:

```python
with connection.cursor() as cursor:
   cursor.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;")
   cursor.execute("SELECT ... ")
   # ...
```

### <a name="solution3"></a>Solution 3: Use `select_for_update()` for Complex Queries

Reading and updating an object through multiple steps is a very common use case and is supported by modern relational databases, thanks to the `SELECT ... FOR UPDATE` statement. With this statement, the rows that are selected are locked, preventing any concurrent update until the current transaction is committed

When we try to use this statement, the rows that we are trying to access may be already locked by another transaction. In that case, we have several options:

* wait until the concurrent transaction finishes
* don't wait and return an error (`NOWAIT`)
* skip any locked row (`SKIP LOCKED`)

Django includes a `select_for_update` function [in its Queryset API](https://docs.djangoproject.com/en/5.1/ref/models/querysets/#select-for-update) , with the following signature:

`select_for_update(nowait=False, skip_locked=False, of=(), no_key=False)`

Note that rows of selected objects specified in `select_for_update` are locked in addition to rows of the queryset’s model.

Using this function, we can build a new view that will lock the counter instance to prevent concurrent updates:

```python
import time

from django.db import transaction
from django.http import JsonResponse

from .models import Counter

def increment_counter_lock(request, name):
    with transaction.atomic():
        # Lock the row to prevent concurrent access
        counter = Counter.objects.select_for_update().get(name=name)
        time.sleep(5)
        counter.value += 1
        counter.save()
    return JsonResponse({"name": name, "value": counter.value})
```

Running our test script again, we can see that the counter is properly incremented. However, even if the requests are sent concurrently, they are only executed sequentially due to the lock on the counter table. The screenshot below shows the timestamp when each response is received, with a clear 5-second delay between each response.

![image.png](/images/blog/Avoiding%20Lost%20Updates%20in%20Django/gyqaDFAPfbH3Dl-image.png)

## <a name="conclusion"></a>5. Conclusion

Lost updates are a common issue when using the default **Read Committed** isolation level in relational databases. Ignoring this issue can lead to concurrency bugs that often manifest at higher scales or under heavy load.

In a Django application, you can prevent lost updates using the following techniques:

1. **Switch to Serializable Isolation** for strict guarantees, but with a performance trade-off.
2. **Use **`F()`** expressions** for atomic writes when operations are simple.
3. Leverage `select_for_update()` to lock rows during complex updates.

Choosing the right approach depends on your application's requirements for consistency and performance.

# <a name="references"></a>6. References and Further Reading

Below are resources that provide more context and depth to the topics discussed in this document:

- [Django QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/): Detailed documentation on QuerySet methods, including `select_for_update` and `F()` expressions.  

- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html): Explanation of the different isolation levels supported by PostgreSQL.  

- [MySQL: InnoDB Isolation Levels](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html): Information on MySQL's implementation of isolation levels and their guarantees.  

- ["Designing Data-Intensive Applications" by Martin Kleppmann, Chapter 7](https://martin.kleppmann.com/): An excellent overview of transaction concepts and their implications for developers.  

These resources will help you dive deeper into Django, database isolation levels, and concurrency handling techniques.
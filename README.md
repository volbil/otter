# Otter

Otter is framework for creating microservices in Flask like fassion using [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) communication via message queue. Its built in top of [kiwiPy](https://github.com/aiidateam/kiwipy) library.

## Application

Simple Otter application looks liks this.

```python
from otter import Otter
import hashlib
import time

app = Otter()

@app.add_broadcast(["message.*"])
def example_broadcast(comm, body, sender, subject, correlation_id):
    print(f"Received {body}")

@app.add_task("example.task")
def example_task(comm, delay):
    time.sleep(delay)
    print(f"Done waiting {delay} seconds")

@app.add_rpc("example.hash")
def example_hash(comm, data):
    return {
        "result": hashlib.sha256(
            data.encode("utf-8")
        ).hexdigest()
    }

app.run("amqp://guest:guest@127.0.0.1/", debug=True)
```

## Client

You can communicate with Otter application using `Client`.

```python
from otter import Client

client = Client("amqp://guest:guest@127.0.0.1/")

if client.comm:
    # Broadcast message to anyone who listens
    client.broadcast("otter", subject="message.send")

    # Send task to remote worker
    client.task(5)

    # Send rpc request to hash "otter" and wait for the result
    data = client.rpc("example.hash", "otter").result()

client.close()
```

## Blueprints

You can use Flask like blueprints in order to organize and split your application into different modules.

```python
from otter import Blueprint

blueprint = Blueprint()

@blueprint.add_rpc("hello.world")
def example_hash(comm, data):
    return {"result": "Hello world from blueprint!"}

```

After that blueprint can be initialized using `register_blueprint` method.

```python
app.register_blueprint(blueprint)
```

## Decorators

In most cases you will use JSON to communicate between your microservices, thats why Otter has built in decorator `@use_args` which uses Marshmallow for data validation.

```python
from marshmallow import fields, validate
from otter.decorators import use_args

login_args = {
    "password": fields.Str(required=True, validate=validate.Length(min=8)),
    "email": fields.Email(required=True)
}

@app.add_rpc("auth.login")
@use_args(login_args)
def login(comm, data):
    return {"args": data}

```

### Foreword

This is experimental software, any contributions are welcome!

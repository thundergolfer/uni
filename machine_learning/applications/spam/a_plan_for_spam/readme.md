## _A Plan For Spam_

> Self-education in end-to-end machine learning application engineering, based off
> Paul Graham's early 2000s essay.

### Rules

This code is for education, both of myself and others who care to engage with it. As such,
it has understanding-oriented rules.

1. 'From scratch'. No 3rd-party libraries or frameworks (stdlib OK). Write a basic version of what's needed.
2. Run locally. Let's avoid the pain and added complexity of Docker, Kubernetes, AWS, etc.
3. End-to-end, deliver business value. Don't build only the model. The model is not an application.

### Business Problem

Spam.

### System overview

> Components, and how they connect.

#### Components

1. Mail server (incoming / outgoing)
2. Spam detection API server
3. Email user activity simulation server 
4. Data warehouse
5. Model trainer

#### Diagram

TODO

### Usage

`python3 agent.py start`

Will open multiple terminal windows running the various parts of the system.

Be aware, they may open up all on top of each other, making it look like just one opened.

### Development

#### Testing

The application code is all pure-Python (stdlib only), but testing uses `pytest`. 

`python3 -m pytest` ('-m' method adds current dir to `sys.path`)

or, for just **integration**:

`python3 -m pytest integration/`

#### Type-checking

At the moment, I haven't got a virtualenv so `mypy` is installed to system. 🤮

`mypy --namespace-packages *.py`

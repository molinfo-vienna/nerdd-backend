<h1 align="center">
    nerdd-backend
</h1>

<p align="center" style="margin-top: 25px; font-size: 20px;">

</p>

<hr/>

<div align="center">

![GitHub tag](https://img.shields.io/github/v/tag/molinfo-vienna/nerdd-backend
)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fshirte%2Fnerdd-backend%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
![FastAPI](https://img.shields.io/badge/-FastAPI-059487?logo=fastapi&logoColor=white&style=flat-square
)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)
![GitHub License](https://img.shields.io/github/license/molinfo-vienna/nerdd-backend)

</div>

<div align="center">
<a href="https://github.com/molinfo-vienna/nerdd-module">📦 nerdd-module</a>
•
<a href="https://github.com/molinfo-vienna/nerdd-link">🔗 nerdd-link</a>
•
<a href="https://github.com/molinfo-vienna/nerdd">⚙️ Infrastructure</a>
•
<a href="https://nerdd.univie.ac.at">🌐 NERDD website</a>
</div>

<br/>


## Usage

```sh
# create conda environment
conda env create -f environment.yml
conda activate nerdd_backend

# install dependencies
cd nerdd-backend
pip install .

# run with a toy communication channel, database backend and a basic computational module (quickstart)
python -m nerdd_backend.main

# use localhost:8000 for api requests
curl localhost:8000/modules

# see all endpoints at API docs at http://localhost:8000/docs
xdg-open http://localhost:8000/docs
```


## Settings

```sh
# change port
python -m nerdd_backend.main ++port=7999

# turn off fake data
python -m nerdd_backend.main ++mock_infra=false

# set storage directory
python -m nerdd_backend.main ++media_root=./media

# run on existing kafka cluster as communication channel and rethinkdb database backend
# (see all options in config files in settings folder)
python -m nerdd_backend.main --config-name production \
  ++db.host=localhost ++db.port=31562 \
  ++channel.broker=localhost:31624
```

## Architecture

![Architecture Diagram](./assets/nerdd-backend-architecture-light.png#gh-light-mode-only)
![Architecture Diagram](./assets/nerdd-backend-architecture-dark.png#gh-dark-mode-only)

* The subpackage `nerdd_backend.routers` contains all FastAPI routes accessible by the user.
* All routes have access to the FastAPI application state using `request.app.state` containing
  * `state.config`: custom settings (e.g. `max_num_molecules_per_job`) provided by the user when starting the server,
  * `state.repository`: the database access layer,
  * `state.channel`: an object for sending messages to the message broker, and
  * `state.filesystem`: an object for storing and retrieving files.
* Application settings are managed using [Hydra](https://github.com/facebookresearch/hydra). 
  Predefined configurations are defined in `/settings`, but individual options may be overridden 
  when starting the server application.
* All schemas of requests, responses and records persisted to the database are declared as Pydantic 
  models (deriving from `pydantic.BaseModel`) in `nerdd_backend.models`.
* The `nerdd_backend.data.Repository` class represents the database access layer specifying all 
  database interactions. For a concrete database, a subclass of `Repository` is defined and all 
  required methods are implemented. This abstraction allows the replacement of the underlying 
  database technology without changes to the application logic.
* Communication with the NERDD infrastructure is handled via a message broker. The package 
  `nerdd-link` defines message schemas and available topics. Specifically, the `nerdd_link.Action` 
  class allows iterating over all messages in a topic and processing them using custom logic. All 
  files in the `nerdd_backend.actions` subpackage contain subclasses of `nerdd-link.Action` that 
  react to messages coming from the message broker. 
* Actions are executed asynchronously in the global FastAPI lifespan, i.e. they run in parallel 
  to FastAPI's handlers that serve HTTP requests.


## Contribute

```sh
# create conda environment
conda env create -f environment.yml

# install package in development mode
pip install -e .[test]

# run tests
pytest

# run tests with automatic reload on code changes
ptw
```
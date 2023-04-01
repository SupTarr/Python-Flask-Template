# Python Flask Template

## About The Project

This project was completed as part of `Flask: Develop Web Applications in Python` form `educative`. I am tasked to make full use of Flask and Python knowledge and its accompanying documentation to create an a website for a fictional animal rescue organization.

## Technologies

This project was created with:

- Python
- Flask
- PostgreSQL

## Installation

### Run Locally

Clone the project

```sh
git clone https://github.com/SupTarr/Python-FastAPI-Template.git
```

### Virtual environment on windows

To install `virtualenv` via pip

```cmd
py -m pip install --user virtualenv
```

To create a `virtual environment` for your project, open a new command prompt, navigate to the folder where you want to create your project and then enter the following:

```cmd
py -m virtualenv .
```

To activate the environment, run:

```cmd
.\Scripts\activate.bat
```

(Python-FastAPI-Template) C:\Users\tatas\Desktop\SupTarr\Workspace\Python-FastAPI-Template>

In the command prompt, ensure your virtual environment is active, and execute the following command:

```cmd
pip install -r requirements.txt
```

### FastAPI

```cmd
uvicorn app.main:app --reload
```

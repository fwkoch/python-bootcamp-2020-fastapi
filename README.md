# Microservices with FastAPI

Prepared for Calgary / Edmonton Python Bootcamp 2020

## Prerequisites

- Knowledge of Python basics
    - variables, naming convention, loops, functions, classes,
      object-oriented programming, testing, best practices
    - Attendance at sessions 1 and 2 of the bootcamp is satisfactory
- Understanding of RESTful web APIs
    - What are RESTful APIs? How do we start thinking about them
      in Python?
    - Provided by [Zero To API](https://github.com/dgmouris/zero_to_api)

## Environment

- Virtual environment with Python 3.7+ (I will probably use [conda](https://www.anaconda.com/))
- [Jupyter notebook](https://jupyter.org/) or [Google Colab](https://colab.research.google.com/)
- IDE for writing code (I will probably use [sublime](https://www.sublimetext.com/))
- Terminal for executing code (likely this is possible from the IDE, but
  I will just use basic mac terminal)
- RESTful client (I usually just use Jupyter notebooks and Python requests)

_Note:_ The setup from [Zero To API](https://github.com/dgmouris/zero_to_api#prerequistes-to-follow-the-presentation)
should be satisfactory for this presentation as well, as long as Python is
3.7+.

## Overview

- We will start by covering a few additional prerequisite topics for
  understanding FastAPI
    - [Access notebook in Google Colab](https://colab.research.google.com/drive/1xgTVIWOKUu2IlEES4aA17yPkrUxMLyex)
    - Declarative programming with [dataclasses](https://docs.python.org/3/library/dataclasses.html) and [pydantic](https://pydantic-docs.helpmanual.io/)
    - [Decorators](https://www.datacamp.com/community/tutorials/decorators-python)
    - Async with [asyncio](https://docs.python.org/3/library/asyncio.html)
- Next, we will then talk about microservices
    - Pros, cons, comparison to monolith and realistic architectures
    - No coding for this part!
- Finally, [FastAPI](https://fastapi.tiangolo.com/)!
    - What is it? Why is it great?
    - Building an example application together
    - We will consume the [NHL API](https://gitlab.com/dword4/nhlapi/-/tree/master)
    - Notebook to access API [here](https://colab.research.google.com/drive/15UVwvHS6-rUUHD53bfns_Kl4ZwZEEjP2)
        - Note: This will not actually work in Google Colab, you can only
          access `localhost` locally.

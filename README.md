[![Language](https://img.shields.io/badge/language-python-blue.svg)]()
[![Build Status](https://travis-ci.org/jtrejo13/matlab-interpreter.svg?branch=master)](https://travis-ci.org/jtrejo13/matlab-interpreter)
[![Codecov](https://img.shields.io/codecov/c/github/jtrejo13/matlab-interpreter.svg)]()

# MATLAB interpreter

A (simplified) MATLAB language interpreter. 

## About

This interpreter was written in Python and it directly executes instructions written in the MATLAB language. The interpreter uses the following strategies for program execution:

1) Reads and 'tokenizes' the input source code
2) Parses the tokenized source code and produces an Abstract Syntax Tree (AST)
3) Traverses and interprets the AST, executing expressions as it moves along the tree

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Requirements for execution:

```
python (3.5)
pip (8.1.2)
make (4.0)
autopep8 (1.2.4)
coverage (4.2)
numpy (1.11.1)
pep8 (1.7.0)
pip (8.1.2)
pylint (1.6.4)
mypy
astroid (1.4.8)
pydoc3.5

```

### Installation

A step by step series of examples that tell you have to get a development env running

#### Option 1: Virtual Environment

This option assumes python and pip (v3) are installed in your machine.

1) Install the virtual environment library (virtualenv) via pip:

```bash
$ pip install virtualenv
```

2) Test your installation:

```bash
$ virtualenv --version
```

3) Create a virtual environment for a project:

```bash
$ cd my_project_folder
$ virtualenv env
```

4) To begin using the virtual environment, it needs to be activated:

```bash
$ source env/bin/activate
```

5) And requirements need to be installed:

```bash
$ pip install -r requirements.txt
```
6) After installing the requirements, you are ready to execute the interpreter:

```bash
$ execute
```

#### Option 2: Docker - Virtual Machine

1) Download and install Docker [here](https://www.docker.com/community-edition#/download)

2) Verify that installation was successful:

```bash
$ docker --version
```

3) Pull the following image for the virtual machine:
```bash
$ docker pull gpdowning/python
```

4) Verify successful pull:
```bash
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
gpdowning/python    latest              9e0a05a1bd40        7 days ago          783.1 MB
python              3.5.2               58528474c16a        2 weeks ago         683.2 MB
```

5) Run docker within project directory:
```bash
$ cd my_project_folder
$ pwd
$ my_project_folder_full_path
$ docker run -it -v my_project_folder_full_path:/usr/user_name -w /usr/user_name gpdowning/python
```

6) After successfully running virtual machine, you are ready to execute the interpreter:

```bash
$ execute
```

## Tools

* [Python 3](https://docs.python.org/3/) - The programming language
* [Make](https://www.gnu.org/software/make/) - Automated builds
* [Git](https://www.git-scm.com/) - Source control
* [Pylint](https://www.pylint.org/) - Code static analysis
* [unittest](https://docs.python.org/3.5/library/unittest.html) - Unit testing
* [coverage](https://pypi.python.org/pypi/coverage) - Code coverage
* [Pydoc](https://docs.python.org/3.4/library/pydoc.html) - Automated documentation
* [autopep8](https://pypi.python.org/pypi/autopep8) - Automated formatting
* [TravisCI](https://education.travis-ci.com/) - Continious integration


## Versioning

For the versions available, see the [tags on this repository](https://github.com/jtrejo13/matlab-interpreter/releases). 

## Author

* **Juan Trejo**
- [GitHub](https://github.com/jtrejo13)
- [LinkedIn](https://www.linkedin.com/in/jtrejo13/)
- [Home](https://jtrejo13.github.io/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspired by [rspivak](https://github.com/rspivak) and his 'Let's Build a Simple Pascal Interpreter' [project](https://github.com/rspivak/lsbasi)

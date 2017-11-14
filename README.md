[![Build Status](https://travis-ci.org/jtrejo13/matlab-interpreter.svg?branch=master)](https://travis-ci.org/jtrejo13/matlab-interpreter)
[![Language](https://img.shields.io/badge/language-python-blue.svg)]()

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

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
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

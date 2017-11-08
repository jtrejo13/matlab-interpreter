.DEFAULT_GOAL := all

FILES1 :=               \
    Interpreter         \
    RunInterpreter      \
    TestInterpreter

FILES2 :=           \
    Interpreter.html    \
    Interpreter.log     \
    Interpreter.py      \
    RunInterpreter.in   \
    RunInterpreter.out  \
    RunInterpreter.py   \
    TestInterpreter.py

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    MYPY     := mypy
    COVERAGE := coverage
    PYDOC    := pydoc
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip
    MYPY     := mypy
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    MYPY     := mypy
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    MYPY     := mypy
    PYLINT   := pylint3
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif

.pylintrc:
		$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

Interpreter.html: Interpreter.py
		$(PYDOC) -w Interpreter

Interpreter.log:
		git log > Interpreter.log

%: %.py .pylintrc
		-$(MYPY)   $<
		-$(PYLINT) $<

RunInterpreter.pyx: Interpreter RunInterpreter
		$(PYTHON) RunInterpreter.py < RunInterpreter.in > RunInterpreter.tmp
		-diff RunInterpreter.tmp RunInterpreter.out

TestInterpreter.pyx: Interpreter TestInterpreter .pylintrc
		-$(COVERAGE) run    --branch TestInterpreter.py
		-$(COVERAGE) report -m


all: $(FILES1)

check: $(FILES2)

clean:
		rm -f  .coverage
		rm -f  .pylintrc
		rm -f  *.pyc
		rm -f  *.tmp
		rm -rf __pycache__
		rm -rf .mypy_cache

config:
		git config -l

docker:
		docker run -it -v $(PWD):/usr/interpreter -w /usr/interpreter gpdowning/python

format:
		$(AUTOPEP8) -i Interpreter.py
		$(AUTOPEP8) -i RunInterpreter.py
		$(AUTOPEP8) -i TestInterpreter.py

run: RunInterpreter.pyx TestInterpreter.pyx

scrub:
		make clean
		rm -f Interpreter.html
		rm -f Interpreter.log

status:
		make clean
		@echo
		git branch
		git remote -v
		git status

travis: Interpreter.html Interpreter.log
		make clean
		ls -al
		make run
		ls -al
		make -r check

versions:
	which cmake
	cmake --version
	@echo
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(MYPY)
	$(MYPY) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list
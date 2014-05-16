Python-Flask-Stack
==================

Requirements
============

Python 2.7 with distutils and virtualenv installed.


Usage
=====

The repo must be included as a submodule to your main git repo.
It can be named anything. Assume it is called "src". The top level
of the repo must include a wscript file which should look like:


```python
APPNAME = <APPNAME>
VERSION = <VERSION>

top = "."
out = "env"


def options(ctx):
    ctx.recurse("src")


def configure(ctx):
    ctx.recurse("src")


def build(ctx):
    ctx(rule="virtualenv --distribute .", target="bin/python")
    ctx.template(
        "src/activate.tmpl", format=False, executable=True,
        source="bin/python", target="bin/activate")

    ctx.recurse("src")
```

To build the stack, run the following command from the top level of the repo.

On Ubuntu, you must first install a fortran compiler with lapack.

```
$ sudo apt-get install python-virtualenv
```

To build the stack run:

```
$ src/waf configure clean build
```

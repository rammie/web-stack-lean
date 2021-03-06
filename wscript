#! /usr/bin/env python
# encoding: utf-8
import os
import platform
import sys


def options(ctx):
    toolsdir = os.path.join(ctx.path.abspath(), "waftools")
    ctx.load("venv", tooldir=toolsdir)
    ctx.load("modules", tooldir=toolsdir)


def configure(ctx):
    print("→ configuring the project in " + ctx.path.abspath())
    toolsdir = os.path.join(ctx.path.abspath(), "waftools")
    ctx.load("venv", tooldir=toolsdir)
    ctx.load("modules", tooldir=toolsdir)
    ctx.env.SRCPATH = ctx.path.abspath()


def build(ctx):
    ctx.module(
        "pkg-config-0.27.1", "--disable-debug --with-internal-glib",
        source="../bin/activate", target="../bin/pkg-config")

    ctx.module("libpng-1.5.13", source="../bin/pkg-config", target="../bin/libpng-config")
    ctx.module("zeromq-3.2.2", source="../bin/pkg-config", target="../lib/libzmq.a")
    ctx.module("node-v0.10.22", source="../bin/pkg-config", target="../bin/node")
    ctx.module("bmc-daemonize-9378868", source="../bin/pkg-config", target="../sbin/daemonize")
    ctx(rule="ln -sf ../${SRC} ${TGT}", source="../sbin/daemonize", target="../bin/daemonize")
    ctx(rule=ctx.build_postgresql, source="../bin/pkg-config", target="../bin/postmaster")
    ctx(rule=ctx.build_redis, source="../bin/pkg-config", target="../bin/redis-server")

    platform_deps = []
    pkg = os.path.join(ctx.path.abspath(), "3rdparty", "site-packages")
    if sys.platform == "darwin" and platform.mac_ver()[0] < "10.9":
        # Readline does not build on Mavericks and is no longer needed.
        readlinetar = "%s/readline-6.2.4.1.tar.gz" % pkg
        readlinecmd = ctx.venv("easy_install --no-find-links %s && touch ${TGT}" % readlinetar)
        ctx(rule=readlinecmd, source="../bin/pkg-config", target="../.readline-done")
        platform_deps = ["../.readline-done"]

    reqs = "%s/requirements.txt" % ctx.path.abspath()
    ctx(
        rule=ctx.venv("pip install --no-index -f file://%s -r %s && touch ${TGT}" % (pkg, reqs)),
        source=platform_deps + [
            "../bin/libpng-config",
            "../lib/libzmq.a",
            "../bin/postmaster",
            "../bin/redis-server"
        ],
        target="../.requirements-done")
    ctx.add_manual_dependency("../.requirements-done", ctx.path.find_node("requirements.txt"))

    ctx(rule=ctx.venv("npm install -g jshint"), source="../bin/node", target="../bin/jshint")
    ctx(rule=ctx.venv("npm install -g bower"), source="../bin/node", target="../bin/bower")

    ctx(
        rule=ctx.venv("npm install -g uglify-js@2.4.7"),
        source="../bin/node", target="../bin/uglifyjs")

    ctx(
        rule=ctx.venv("npm install -g node-sass@0.9.6"),
        source="../bin/node", target="../bin/node-sass")

    ctx(
        rule=ctx.venv("npm install -g protractor; webdriver-manager update"),
        source="../bin/node", target="../bin/protractor")

    karma = "../lib/node_modules/karma/bin/karma"
    ctx(rule=ctx.venv("npm install -g karma"), source="../bin/node", target=karma)
    ctx(rule=ctx.venv("npm install -g karma-cli"), source=karma,
        target="../lib/node_modules/karma-cli/package.json")
    ctx(rule=ctx.venv("npm install -g karma-coverage"), source=karma,
        target="../lib/node_modules/karma-coverage/package.json")
    ctx(rule=ctx.venv("npm install -g karma-junit-reporter"), source=karma,
        target="../lib/node_modules/karma-junit-reporter/package.json")
    ctx(rule=ctx.venv("npm install -g karma-ng-scenario"), source=karma,
        target="../lib/node_modules/karma-ng-scenario/package.json")
    ctx(rule=ctx.venv("npm install -g karma-chrome-launcher"), source=karma,
        target="../lib/node_modules/karma-chrome-launcher/package.json")
    ctx(rule=ctx.venv("npm install -g karma-firefox-launcher"), source=karma,
        target="../lib/node_modules/karma-firefox-launcher/package.json")
    ctx(rule=ctx.venv("npm install -g karma-phantomjs-launcher"), source=karma,
        target="../lib/node_modules/karma-phantomjs-launcher/package.json")
    ctx(rule=ctx.venv("npm install -g karma-jasmine"), source=karma,
        target="../lib/node_modules/karma-jasmine/package.json")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   This is a Python API for the Nitrate test case management system.
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
#   Author: Petr Splichal <psplicha@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
High-level API for the Nitrate test case management system.

This module provides a high-level python interface for the nitrate
module. Handles connection to the server automatically, allows to set
custom level of logging and data caching. Supports results coloring.


Config file
~~~~~~~~~~~

To be able to contact the Nitrate server a minimal user configuration
file ~/.nitrate has to be provided in the user home directory:

    [nitrate]
    url = https://nitrate.server/xmlrpc/

It's also possible to provide system-wide config in /etc/nitrate.conf.


Logging
~~~~~~~

Standard log methods from the python 'logging' module are available
under the short name 'log', for example:

    log.debug(message)
    log.info(message)
    log.warn(message)
    log.error(message)

By default, messages of level WARN and up are only displayed. This can
be controlled by setting the current log level. See setLogLevel() for
more details. In addition, you can easily display info messages using:

    info(message)

which prints provided message (to the standard error output) always,
regardless the current log level. To get a brief overview about current
status use 'print Nitrate()' which gives a short summary like this:

    Nitrate server: https://nitrate.server/xmlrpc/
    Total requests handled: 0


MultiCall support
~~~~~~~~~~~~~~~~~

MultiCall feature is used to encapsulate multiple calls to a remote
server into a single request. If enabled, TestPlan, TestRun, TestCase
and CaseRun objects will use MultiCall for updating their states (thus
speeding up the process). Example usage:

    multicall_start()
        for caserun in TestRun(12345):
            caserun.status = Status("IDLE")
            caserun.update()
    multicall_end()

When multicall_start() is called, update queries are not sent
immediately to server. Instead, they are queued and after
multicall_end() is called, all queries are sent to server in a batch.


Caching support
~~~~~~~~~~~~~~~

In order to save calls to server and time, caching support has been
implemented. Every class that handles objects has its own cache and it is used
to save already initialized (fetched) objects from server. Several classes are
automatically fetched from server after initialization (immutable objects), the
rest will be fetched from server upon request.

Currently, there are 3 types (levels) of caching:

    CACHE_NONE - no caching at all
    CACHE_CHANGES - caching only local updates of instance attributes
    CACHE_OBJECTS - caching objects for further use (default setting)
    CACHE_PERSISTENT - persistent caching (caching in a file) option enabled

Methods that manipulate caching levels:

    get_cache_level()
    set_cache_level()

Persistent cache (local proxy) was another idea how to speed up performance of
the module. It allows class caches to be stored in a file, load caches from a
file, and clear caches. This performance improvement is very helpful mainly for
immutable classes (for example User), where all user can be imported in the
beggining of a script and a lot of connections can be saved.

This performance improvement can be activated only by specifying file name in
config section ([cache]).

Cache expiration is a way how to prevent using probably obsoleted object (for
example caserun). Every class has its own default expiration time, but, of
course, it can be modified from config file (see example in [expiration])
and user input. Time unit in cache expiration is 1 hour.

User can specify the expiration time for class using:

    class.set_expiration(time)

There are two special values:

     0: EXPIRE_ALWAYS -> no caching of certain class
    -1: EXPIRE_NEVER -> object never expires

Default values for specific classes:

    Build ...... 12 months
    Category ... 12 months
    PlanType ... 12 months
    Product .... 12 months
    User ....... 24 months
    Version .... 12 months

    TestPlan ... 2 days
    TestRun .... 12 hours
    TestCase ... 12 hours
    CaseRun .... 1 hour


Search support
~~~~~~~~~~~~~~

Multiple Nitrate classes provide the static method 'search' which takes
the search query in the Django QuerySet format which gives an easy
access to the foreign keys and basic search operators. For example:

    Product.search(name="Red Hat Enterprise Linux 6")
    TestPlan.search(name__contains="python")
    TestRun.search(manager__email='login@example.com'):
    TestCase.search(script__startswith='/CoreOS/python')

For the complete list of available operators see Django documentation:
https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups


Test suite
~~~~~~~~~~~

For running the unit test suite additional sections are required in the
configuration file. These contain the url of the test server and the
data of existing objects to be tested, for example:

    [test]
    url = https://test.server/xmlrpc/

    [product]
    id = 60
    name = Red Hat Enterprise Linux 6

    [component]
    id = 123
    name = wget
    product = Red Hat Enterprise Linux 6

    [testplan]
    id = 1234
    name = Test plan
    type = Function
    product = Red Hat Enterprise Linux 6
    version = 6.1
    status = ENABLED

    [plantype]
    id = 1
    name = General

    [testrun]
    id = 6757
    summary = Test Run Summary

    [testcase]
    id = 1234
    summary = Test case summary
    product = Red Hat Enterprise Linux 6
    category = Sanity

    [expiration]
    user = -1
    caserun = 1
    tag = 24000

    [cache]
    file = /tmp/data.pkl

To exercise the whole test suite just run "python nitrate.py". To test
only subset of tests pick the desired classes on the command line:

    python -m nitrate.api TestCase


Performance tests
~~~~~~~~~~~~~~~~~~

For running the performance test suite an additional section containing
information about the test bed is required:

    [performance]
    testplan = 1234
    testrun = 12345

Use the test-bed-prepare.py script attached in the test directory to
prepare the structure of test plans, test runs and test cases. To run
the performance test suite use --performance command line option.
"""

from api import *

__all__ = """
        Nitrate Mutable
        Product Version Build
        Category Priority User Bug Tag
        TestPlan PlanType PlanStatus
        TestRun RunStatus
        TestCase CaseStatus
        CaseRun Status Cache

        ascii color listed pretty
        log info setLogLevel
        setCacheLevel CACHE_NONE CACHE_CHANGES CACHE_OBJECTS CACHE_PERSISTENT
        setColorMode COLOR_ON COLOR_OFF COLOR_AUTO
        set_log_level set_cache_level set_color_mode
        get_log_level get_cache_level get_color_mode
        multicall_start multicall_end
        """.split()

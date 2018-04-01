#  Copyright (c) 2015-2017 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import os
import random
import shutil
import string
import tempfile

import pytest

from molecule import config
from molecule import logger
from molecule import util

LOG = logger.get_logger(__name__)

pytest_plugins = ['helpers_namespace']


@pytest.helpers.register
def run_command(cmd, env=os.environ, log=True):
    if log:
        cmd = _rebake_command(cmd, env)

    return util.run_command(cmd)


def _rebake_command(cmd, env, out=LOG.out, err=LOG.error):
    return cmd.bake(_env=env, _out=out, _err=err)


@pytest.fixture
def random_string(l=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(l))


@pytest.fixture
def temp_dir(tmpdir, random_string, request):
    directory = tmpdir.mkdir(random_string)
    os.chdir(directory.strpath)

    def cleanup():
        shutil.rmtree(directory.strpath)

    request.addfinalizer(cleanup)

    return directory


@pytest.helpers.register
def molecule_project_directory():
    return os.getcwd()


@pytest.helpers.register
def molecule_directory():
    return config.molecule_directory(molecule_project_directory())


@pytest.helpers.register
def molecule_scenario_directory():
    return os.path.join(molecule_directory(), 'default')


@pytest.helpers.register
def molecule_file():
    return get_molecule_file(molecule_scenario_directory())


@pytest.helpers.register
def get_molecule_file(path):
    return config.molecule_file(path)


@pytest.helpers.register
def molecule_ephemeral_directory():
    project_directory = 'test-project'
    scenario_name = 'test-instance'

    return os.path.join(tempfile.gettempdir(), 'molecule', project_directory,
                        scenario_name)


def pytest_addoption(parser):
    parser.addoption(
        '--delegated', action='store_true', help='Run delegated driver tests.')

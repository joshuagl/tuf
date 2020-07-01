#!/usr/bin/env python

# Copyright 2014 - 2017, New York University and the TUF contributors
# SPDX-License-Identifier: MIT OR Apache-2.0

"""
<Program Name>
  test_tuf_api.py

<Author>
  Joshua Lock <jlock@vmware.com>

<Started>
  June 30, 2020.

<Copyright>
  See LICENSE-MIT OR LICENSE for licensing information.

<Purpose>
  Unit tests for tuf.api
"""

# Help with Python 3 compatibility, where the print statement is a function, an
# implicit relative import is invalid, and the '/' operator performs true
# division.  Example:  print 'hello world' raises a 'SyntaxError' exception.
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest
import logging
import tempfile
import shutil
import sys
import errno
import os

from tuf.api import metadata

from dateutil.relativedelta import relativedelta
import iso8601
import six

logger = logging.getLogger(__name__)


class TestTufApi(unittest.TestCase):
  @classmethod
  def setUpClass(cls):

    # Create a temporary directory to store the repository, metadata, and target
    # files.  'temporary_directory' must be deleted in TearDownClass() so that
    # temporary files are always removed, even when exceptions occur.
    cls.temporary_directory = tempfile.mkdtemp(dir=os.getcwd())
    test_repo_data = os.path.join('repository_data', 'repository')
    cls.repo_dir = os.path.join(cls.temporary_directory, 'repository')
    shutil.copytree(test_repo_data, cls.repo_dir)



  @classmethod
  def tearDownClass(cls):

    # Remove the temporary repository directory, which should contain all the
    # metadata, targets, and key files generated for the test cases.
    shutil.rmtree(cls.temporary_directory)


  def test_metadata_snapshot(self):
    snapshot = metadata.Snapshot()
    snapshot.read_from_json(os.path.join(self.repo_dir, 'metadata.staged', 'snapshot.json'))

    self.assertEqual(snapshot.version, 1)
    snapshot.bump_version()
    self.assertEqual(snapshot.version, 2)

    self.assertEqual(snapshot.expiration, iso8601.parse_date("2030-01-01T00:00:00Z"))
    snapshot.bump_expiration()
    self.assertEqual(snapshot.expiration, iso8601.parse_date("2030-01-02T00:00:00Z"))
    snapshot.bump_expiration(relativedelta(years=1))
    self.assertEqual(snapshot.expiration, iso8601.parse_date("2031-01-02T00:00:00Z"))

    # snapshot.update()

    # snapshot.signable()

    # snapshot.sign()

    # snapshot.verify()

    # snapshot.write_to_json(os.path.join(cls.temporary_directory, 'api_snapshot.json'))

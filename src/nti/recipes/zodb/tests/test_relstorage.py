#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904


from hamcrest import assert_that
from hamcrest import is_
from hamcrest import has_key
from hamcrest import has_entry
from hamcrest import contains_string

import zc.buildout.buildout
import zc.buildout.testing

import unittest
import os
from ..relstorage import Databases

class NoDefaultBuildout(zc.buildout.testing.Buildout):
	# The testing buildout doesn't provide a way to
	# ignore local defaults, which makes it system dependent, which
	# is clearly wrong
	def __init__(self):
		zc.buildout.buildout.Buildout.__init__(
            self,
			'',
			[('buildout', 'directory', os.getcwd())],
			user_defaults=False)

class TestDatabases(unittest.TestCase):

	def test_parse(self):
		# No verification, just sees if it runs

		buildout = NoDefaultBuildout()
		buildout['deployment'] = {
			'etc-directory': '/etc',
			'data-directory': '/data'
		}
		buildout['environment'] = {
			'sql_user': 'user',
			'sql_passwd': 'passwd',
			'sql_host': 'host',
			'cache_servers': 'cache'
		}
		buildout['relstorages_opts'] = {
			'sql_user': 'BAZ'
		}
		buildout['relstorages_users_storage_opts'] = {
			'sql_user': 'FOO'
		}
		Databases( buildout, 'relstorages', {'storages': 'Users Users_1 Sessions'} )

		$buildout.print_options()
		assert_that( buildout['relstorages_users_storage']['client_zcml'],
					 contains_string('shared-blob-dir false') )

		assert_that( buildout['relstorages_users_storage']['client_zcml'],
					 contains_string( 'FOO' ) )
		assert_that( buildout['relstorages_users_1_storage']['client_zcml'],
					 contains_string( 'BAZ' ) )

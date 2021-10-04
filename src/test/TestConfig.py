#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys
import os

import qralchemy.config

class TestConfig(unittest.TestCase):
    def runTest(self):
        try:
            os.mkdir('tmp')
        except:
            pass

        self.test_get_config()
        self.test_update_config()
        self.test_delete_config()

    def test_get_config(self):
        '''test get_config'''
        qralchemy.config.set_sys_configfile('data/TestConfig/sys_qralchemy.conf')
        qralchemy.config.set_user_configfile('data/TestConfig/user_qralchemy.conf')

        config = qralchemy.config.get_config()
        self.assertEqual(config['action_map']['sysconfig'], ['System Default'])
        self.assertEqual(config['action_map']['userconfig'], ['System Default'])

    def test_update_config(self):
        '''test update config'''
        qralchemy.config.set_sys_configfile('data/TestConfig/sys_qralchemy.conf')
        qralchemy.config.set_user_configfile('tmp/user_qralchemy.conf')

        qralchemy.config.update_config('action_map', 'bob', 'None')
        config = qralchemy.config.get_config()
        self.assertEqual(config['action_map']['bob'], ['None'])

    def test_delete_config(self):
        '''test delete config'''
        qralchemy.config.set_sys_configfile('data/TestConfig/sys_qralchemy.conf')
        qralchemy.config.set_user_configfile('tmp/user_qralchemy.conf')

        qralchemy.config.update_config('action_map', 'userconfig', '')
        config = qralchemy.config.get_config()
        self.assertNotIn('userconfig', config['action_map'])

def main():
    suite = unittest.TestSuite()
    suite.addTest(TestConfig())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys

import qralchemy.config
import qralchemy.process

class TestProcess(unittest.TestCase):
    def runTest(self):
        self.test_qr_image_handler()
        self.test_qr_get_header()
        self.test_qr_get_action_custom()
        self.test_qr_get_action_default()
        self.test_qr_get_action_nodefault()

    def test_qr_image_handler(self):
        '''test qr_image_handler''' 
        qr_code=qralchemy.process.qr_image_handler('data/TestProcess/bob.png')
        self.assertEqual(qr_code, 'bob:Is not steve\n')

    def test_qr_get_header(self):
        '''test qr_get_header''' 
        header=qralchemy.process.qr_get_header('bob:test')
        self.assertEqual(header, 'bob')

    def test_qr_get_action_custom(self):
        '''test qr_get_action custom action''' 
        qralchemy.config.set_sys_configfile('data/TestProcess/sys_qralchemy.conf')
        qralchemy.config.set_user_configfile('data/TestProcess/user_qralchemy.conf')

        action=qralchemy.process.qr_get_action('sysconfig')
        self.assertEqual(action, ['Program', 'ls'])

    def test_qr_get_action_default(self):
        '''test qr_get_action default action''' 
        qralchemy.config.set_sys_configfile('data/TestProcess/sys_qralchemy.conf')
        qralchemy.config.set_user_configfile('data/TestProcess/user_qralchemy.conf')

        action=qralchemy.process.qr_get_action('asdf')
        self.assertEqual(action, ['None'])

    def test_qr_get_action_nodefault(self):
        '''test qr_get_action nodefault action''' 
        qralchemy.config.set_sys_configfile('data/TestProcess/user_qralchemy.conf')
        qralchemy.config.set_user_configfile('data/TestProcess/user_qralchemy.conf')

        action=qralchemy.process.qr_get_action('asdf')
        self.assertEqual(action, ['System Default'])

def main():
    suite = unittest.TestSuite()
    suite.addTest(TestProcess())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

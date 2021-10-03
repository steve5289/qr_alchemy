#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys
import os

import qralchemy.saved

class TestSaved(unittest.TestCase):
    def runTest(self):
        try:
            os.mkdir('tmp')
        except:
            pass

        qralchemy.saved.set_savefile('tmp/saved.dat')
        self.test_get_saved_codes_empty()
        self.test_set_saved_code()
        self.test_delete_saved_code()

    def test_get_saved_codes_empty(self):
        '''get_saved_codes: empty''' 
        saved_codes=qralchemy.saved.get_saved_codes()

        self.assertEqual(saved_codes, dict())

    def test_set_saved_code(self):
        '''set_saved_code''' 
        
        qralchemy.saved.set_saved_code('label', 'thing')
        saved_codes=qralchemy.saved.get_saved_codes()

        self.assertEqual(saved_codes, {'label' : 'thing'})
        self.assertTrue(qralchemy.saved.is_code_saved('thing'))
        self.assertEqual(qralchemy.saved.get_code_saved_name('thing'), 'label')

    def test_delete_saved_code(self):
        '''delete_saved_code''' 
        
        qralchemy.saved.set_saved_code('label', 'thing')
        qralchemy.saved.delete_saved_code('label')
        saved_codes=qralchemy.saved.get_saved_codes()

        self.assertEqual(saved_codes, dict())
        self.assertFalse(qralchemy.saved.is_code_saved('thing'))

def main():
    suite = unittest.TestSuite()
    suite.addTest(TestSaved())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

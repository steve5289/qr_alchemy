#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys

import qralchemy.history

class Testhistory(unittest.TestCase):
    def runTest(self):
        try:
            os.mkdir('tmp')
        except:
            pass

        qralchemy.history.set_histfile('tmp/history.dat')
        self.test_get_history()

    def test_get_history(self):
        '''get_history''' 
        history = qralchemy.history.get_history()
        self.assertEqual(history, list())

    def test_add_history(self):
        '''add_history''' 
        qralchemy.history.add_history('bob')
        history = qralchemy.history.get_history()
        self.assertEqual(len(history), 1)

    def test_clear_history(self):
        '''clear_history''' 
        qralchemy.history.add_history('bob')
        qralchemy.history.add_history('asdfasdf')
        qralchemy.history.add_history('pie')
        qralchemy.history.clear_history()
        history = qralchemy.history.get_history()
        self.assertEqual(history, list())

def main():
    suite = unittest.TestSuite()
    suite.addTest(Testhistory())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

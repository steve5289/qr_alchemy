#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys

import qr_alchemy.history

class Testhistory(unittest.TestCase):
    def runTest(self):
        try:
            os.mkdir('tmp')
        except:
            pass

        qr_alchemy.history.set_histfile('tmp/history.dat')
        self.test_get_history()

    def test_get_history(self):
        '''get_history''' 
        history = qr_alchemy.history.get_history()
        self.assertEqual(history, list())

    def test_add_history(self):
        '''add_history''' 
        qr_alchemy.history.add_history('bob')
        history = qr_alchemy.history.get_history()
        self.assertEqual(len(history), 1)

    def test_clear_history(self):
        '''clear_history''' 
        qr_alchemy.history.add_history('bob')
        qr_alchemy.history.add_history('asdfasdf')
        qr_alchemy.history.add_history('pie')
        qr_alchemy.history.clear_history()
        history = qr_alchemy.history.get_history()
        self.assertEqual(history, list())

def main():
    suite = unittest.TestSuite()
    suite.addTest(Testhistory())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

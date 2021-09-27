#!/usr/bin/python3
import unittest
from test import support

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import sys

import qr_alchemy.generate

class TestGenerate(unittest.TestCase):
    def runTest(self):
        self.test_generate_valid()
    def test_generate_valid(self):
        '''generate qr code image''' 
        image=qr_alchemy.generate.generate_qr_img('bob')
        self.assertEqual(type(image), qr_alchemy.gui.ResizableImage)

def main():
    unittest.main()

main()

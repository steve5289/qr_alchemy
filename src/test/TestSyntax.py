#!/usr/bin/python3
import unittest
from test import support
import sys


class TestSyntax(unittest.TestCase):
    def runTest(self):
        self.test_load_generate()
        self.test_load_gui()
        self.test_load_config()
        self.test_load_gui_display()
        self.test_load_gui_hist()
        self.test_import_gui_process()
        self.test_import_gui_saved()
        self.test_import_plugins()
        self.test_import_process()
        self.test_import_saved()


    def test_load_generate(self):
        '''import qr_alchemy.generate'''
        import qr_alchemy.generate
        return True

    def test_load_gui(self):
        '''import qr_alchemy.gui''' 
        import qr_alchemy.gui
        return True

    def test_load_config(self):
        '''import qr_alchemy.gui_config''' 
        import qr_alchemy.gui_config
        return True

    def test_load_gui_display(self):
        '''import qr_alchemy.gui_display''' 
        import qr_alchemy.gui_display
        return True

    def test_load_gui_hist(self):
        '''import qr_alchemy.gui_hist''' 
        import qr_alchemy.gui_hist
        return True

    def test_import_gui_process(self):
        '''import qr_alchemy.gui_process''' 
        import qr_alchemy.gui_process
        return True

    def test_import_gui_saved(self):
        '''import qr_alchemy.gui_saved''' 
        import qr_alchemy.gui_saved
        return True

    def test_import_plugins(self):
        '''import qr_alchemy.plugins''' 
        import qr_alchemy.plugins
        return True

    def test_import_process(self):
        '''import qr_alchemy.process''' 
        import qr_alchemy.process
        return True

    def test_import_saved(self):
        '''import qr_alchemy.saved''' 
        import qr_alchemy.saved
        return True

def main():
    suite = unittest.TestSuite()
    suite.addTest(TestSyntax())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

#!/usr/bin/python3
import unittest
from test import support
import sys


class TestSyntax(unittest.TestCase):
    def runTest(self):
        self.test_import_common()
        self.test_import_config()
        self.test_import_generate()
        self.test_import_gui()
        self.test_import_gui_config_general()
        self.test_import_gui_config_actions()
        self.test_import_gui_config_plugins()
        self.test_import_gui_display()
        self.test_import_gui_hist()
        self.test_import_gui_process()
        self.test_import_gui_saved()
        self.test_import_plugins()
        self.test_import_process()
        self.test_import_saved()

    def test_import_common(self):
        '''import qralchemy.common'''
        import qralchemy.common
        return True

    def test_import_config(self):
        '''import qralchemy.gui_config''' 
        import qralchemy.gui_config
        return True

    def test_import_generate(self):
        '''import qralchemy.generate'''
        import qralchemy.generate
        return True

    def test_import_gui(self):
        '''import qralchemy.gui''' 
        import qralchemy.gui
        return True

    def test_import_gui_config_general(self):
        '''import qralchemy.gui_config_general''' 
        import qralchemy.gui_config_general
        return True

    def test_import_gui_config_actions(self):
        '''import qralchemy.gui_config_actions''' 
        import qralchemy.gui_config_actions
        return True

    def test_import_gui_config_plugins(self):
        '''import qralchemy.gui_config_plugins''' 
        import qralchemy.gui_config_plugins

        return True
    def test_import_gui_display(self):
        '''import qralchemy.gui_display''' 
        import qralchemy.gui_display
        return True

    def test_import_gui_hist(self):
        '''import qralchemy.gui_hist''' 
        import qralchemy.gui_hist
        return True

    def test_import_gui_process(self):
        '''import qralchemy.gui_process''' 
        import qralchemy.gui_process
        return True

    def test_import_gui_saved(self):
        '''import qralchemy.gui_saved''' 
        import qralchemy.gui_saved
        return True

    def test_import_plugins(self):
        '''import qralchemy.plugins''' 
        import qralchemy.plugins
        return True

    def test_import_process(self):
        '''import qralchemy.process''' 
        import qralchemy.process
        return True

    def test_import_saved(self):
        '''import qralchemy.saved''' 
        import qralchemy.saved
        return True

def main():
    suite = unittest.TestSuite()
    suite.addTest(TestSyntax())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

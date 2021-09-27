#!/usr/bin/python3
import unittest
from test import support

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf

import qr_alchemy.plugins

class TestPlugins(unittest.TestCase):
    def runTest(self):
        self.test_plugin_list_normal()
        self.test_plugin_list_dirs()
        self.test_plugin_list_empty_dir()
        self.test_plugin_list_file_dir()
        self.test_get_input_plugins()
        self.test_get_output_plugins()
        self.test_run_sys_input_plugins()
        self.test_run_sys_output_plugins()
        self.test_run_user_input_plugins()
        self.test_run_user_output_plugins()

    def test_plugin_list_normal(self):
        '''plugin_list normal plugin dir'''
        plugin_list = qr_alchemy.plugins._get_plugins('data/dir_executables', 'data/dir_executables')
        if 'file1' not in plugin_list:
            self.fail("file1 not found in plugin list:" + ' '.join(plugin_list.keys()))
        if plugin_list['file1'] != "data/dir_executables/file1":
            self.fail("file1 is set to '" + plugin_list['file1'] + "' not 'data/dir_executables/file1'")
        if 'file2' not in plugin_list:
            self.fail("file2 not found in plugin list")
        
    def test_plugin_list_dirs(self):
        '''plugin_list dis with dirs'''
        plugin_list = qr_alchemy.plugins._get_plugins('data/dir_with_dirs', 'data/dir_with_dirs')
        if 'dir1' in plugin_list:
            self.fail("dir1 should not be in: " + ' '.join(plugin_list.keys()))
        
    def test_plugin_list_empty_dir(self):
        '''plugin_list empty dir'''
        plugin_list = qr_alchemy.plugins._get_plugins('data/empty_dir', 'data/empty_dir')
        if plugin_list:
            self.fail("plugin list should be empty: " + ' '.join(plugin_list.keys()))
        
    def test_plugin_list_file_dir(self):
        '''plugin_list dir with files'''
        plugin_list = qr_alchemy.plugins._get_plugins('data/dir_files', 'data/dir_files')
        if plugin_list:
            self.fail("plugin list should be empty: " + ' '.join(plugin_list.keys()))
        
    def test_get_input_plugins(self):
        '''test get_input_plugins'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')
        plugin_list = qr_alchemy.plugins.get_input_plugins()
        if 'sys_input_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'sys_input_plugin.sh' : " + ' '.join(plugin_list.keys()))
        if 'user_input_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'user_input_plugin.sh' : " + ' '.join(plugin_list.keys()))
        
    def test_get_output_plugins(self):
        '''test get_output_plugins'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')
        plugin_list = qr_alchemy.plugins.get_output_plugins()
        if 'sys_output_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'sys_output_plugin.sh' : " + ' '.join(plugin_list.keys()))
        if 'user_output_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'user_output_plugin.sh' : " + ' '.join(plugin_list.keys()))
        
    def test_run_sys_input_plugins(self):
        '''test run_sys_input_plugin'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')

        outfile='tmp/sys_input_plugin.sh'
        qr_alchemy.plugins.run_input_plugin('sys_input_plugin.sh','bob')
        
        if not os.path.isfile(outfile):
            self.fail("Sys input plugin did not create '" +outfile+"'")
        
    def test_run_sys_output_plugins(self):
        '''test run_sys_output_plugin'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')
        rc,code = qr_alchemy.plugins.run_output_plugin('sys_output_plugin.sh')
        self.assertEqual(rc, 0)
        self.assertEqual(code, 'sys_output_plugin.sh\n')
        
    def test_run_user_input_plugins(self):
        '''test run_user_input_plugin'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')

        outfile='tmp/user_input_plugin.sh'
        qr_alchemy.plugins.run_input_plugin('user_input_plugin.sh','bob')
        
        if not os.path.isfile(outfile):
            self.fail("User input plugin did not create '" +outfile+"'")
        
    def test_run_user_output_plugins(self):
        '''test run_user_output_plugin'''

        qr_alchemy.plugins.set_user_plugin_dir('data/user_test_plugins')
        qr_alchemy.plugins.set_sys_plugin_dir('data/sys_test_plugins')
        rc,code = qr_alchemy.plugins.run_output_plugin('user_output_plugin.sh')
        self.assertEqual(rc, 0)
        self.assertEqual(code, 'user_output_plugin.sh\n')
        
def main():
    suite = unittest.TestSuite()
    suite.addTest(TestPlugins())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

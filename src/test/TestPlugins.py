#!/usr/bin/python3
import unittest
from test import support

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf

import qralchemy.plugins

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
        self.test_add_input_plugins()
        self.test_add_output_plugins()

    def test_plugin_list_normal(self):
        '''plugin_list normal plugin dir'''
        plugin_list = qralchemy.plugins._get_plugins('data/TestPlugins/dir_executables', 'data/TestPlugins/dir_executables')
        if 'file1' not in plugin_list:
            self.fail("file1 not found in plugin list:" + ' '.join(plugin_list.keys()))
        if plugin_list['file1'] != "data/TestPlugins/dir_executables/file1":
            self.fail("file1 is set to '" + plugin_list['file1'] + "' not 'data/TestPlugins/dir_executables/file1'")
        if 'file2' not in plugin_list:
            self.fail("file2 not found in plugin list")
        
    def test_plugin_list_dirs(self):
        '''plugin_list dis with dirs'''
        plugin_list = qralchemy.plugins._get_plugins('data/TestPlugins/dir_with_dirs', 'data/TestPlugins/dir_with_dirs')
        if 'dir1' in plugin_list:
            self.fail("dir1 should not be in: " + ' '.join(plugin_list.keys()))
        
    def test_plugin_list_empty_dir(self):
        '''plugin_list empty dir'''
        plugin_list = qralchemy.plugins._get_plugins('data/TestPlugins/empty_dir', 'data/TestPlugins/empty_dir')
        if plugin_list:
            self.fail("plugin list should be empty: " + ' '.join(plugin_list.keys()))
        
    def test_plugin_list_file_dir(self):
        '''plugin_list dir with files'''
        plugin_list = qralchemy.plugins._get_plugins('data/TestPlugins/dir_files', 'data/TestPlugins/dir_files')
        if plugin_list:
            self.fail("plugin list should be empty: " + ' '.join(plugin_list.keys()))
        
    def test_get_input_plugins(self):
        '''test get_input_plugins'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        plugin_list = qralchemy.plugins.get_input_plugins()
        if 'sys_input_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'sys_input_plugin.sh' : " + ' '.join(plugin_list.keys()))
        if 'user_input_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'user_input_plugin.sh' : " + ' '.join(plugin_list.keys()))
        
    def test_get_output_plugins(self):
        '''test get_output_plugins'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        plugin_list = qralchemy.plugins.get_output_plugins()
        if 'sys_output_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'sys_output_plugin.sh' : " + ' '.join(plugin_list.keys()))
        if 'user_output_plugin.sh' not in plugin_list:
            self.fail("plugin list should include 'user_output_plugin.sh' : " + ' '.join(plugin_list.keys()))
        
    def test_run_sys_input_plugins(self):
        '''test run_sys_input_plugin'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')

        outfile='tmp/sys_input_plugin.sh'
        qralchemy.plugins.run_input_plugin('sys_input_plugin.sh','bob')
        
        if not os.path.isfile(outfile):
            self.fail("Sys input plugin did not create '" +outfile+"'")
        
    def test_run_sys_output_plugins(self):
        '''test run_sys_output_plugin'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        rc,code = qralchemy.plugins.run_output_plugin('sys_output_plugin.sh')
        self.assertEqual(rc, 0)
        self.assertEqual(code, 'sys_output_plugin.sh\n')
        
    def test_run_user_input_plugins(self):
        '''test run_user_input_plugin'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')

        outfile='tmp/user_input_plugin.sh'
        qralchemy.plugins.run_input_plugin('user_input_plugin.sh','bob')
        
        if not os.path.isfile(outfile):
            self.fail("User input plugin did not create '" +outfile+"'")
        
    def test_run_user_output_plugins(self):
        '''test run_user_output_plugin'''

        qralchemy.plugins.set_user_plugin_dir('data/TestPlugins/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        rc,code = qralchemy.plugins.run_output_plugin('user_output_plugin.sh')
        self.assertEqual(rc, 0)
        self.assertEqual(code, 'user_output_plugin.sh\n')
        
    def test_add_input_plugins(self):
        '''test add_input_plugin'''

        qralchemy.plugins.set_user_plugin_dir('tmp/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        qralchemy.plugins.add_input_plugin('data/TestPlugins/ex_plugin.sh')

        plugin_list = qralchemy.plugins.get_input_plugins()
        self.assertIn('ex_plugin.sh', plugin_list)

        qralchemy.plugins.delete_input_plugin('ex_plugin.sh')
        plugin_list = qralchemy.plugins.get_input_plugins()
        self.assertNotIn('ex_plugin.sh', plugin_list)
        
    def test_add_output_plugins(self):
        '''test add_output_plugin'''

        qralchemy.plugins.set_user_plugin_dir('tmp/user_test_plugins')
        qralchemy.plugins.set_sys_plugin_dir('data/TestPlugins/sys_test_plugins')
        qralchemy.plugins.add_output_plugin('data/TestPlugins/ex_plugin.sh')

        plugin_list = qralchemy.plugins.get_output_plugins()
        self.assertIn('ex_plugin.sh', plugin_list)

        qralchemy.plugins.delete_output_plugin('ex_plugin.sh')
        plugin_list = qralchemy.plugins.get_output_plugins()
        self.assertNotIn('ex_plugin.sh', plugin_list)
        
def main():
    suite = unittest.TestSuite()
    suite.addTest(TestPlugins())


    result = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    if result:
        sys.exit(0)
    sys.exit(1)
main()

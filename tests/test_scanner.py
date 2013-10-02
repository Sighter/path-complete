import unittest
import Scanner as ScannerM
import os

from os import path
from Scanner import *


class TestScanner(unittest.TestCase):

    def setUp(self):
        
        self.home_dir = os.getenv('HOME')
        self.test_path = path.join(self.home_dir, '.config/sublime-text-2/Packages/Filepath Complete/tests/')
        self.project_path = path.join(self.home_dir, '.config/sublime-text-2/Packages/Filepath Complete/')

        self.oldcwd = os.getcwd()

        os.chdir(self.project_path)

    def tearDown(self):
        
        os.chdir(self.oldcwd)

        self.assertEqual(self.oldcwd, os.getcwd())

    def test_existence(self):
        s = Scanner('  hello world')

        self.assertEqual('hello world', s.line)

    def test_has_PSEP_set_bydefault(self):
        self.assertEqual('/', ScannerM.PSEP)
    
    def test_absolute_prefix(self):

        lines = [
            ('/', '/'),
            ('    /', '/'),
            ('var = "' + self.test_path + '"', self.test_path),
            ('lol = "/', '/'),
            ('... tests /tmp/', '/tmp/'),
            ('... tests /tmp', '/')
        ]

        for (line, should) in lines:
            s = Scanner(line)
            
            self.assertEqual(should, s.get_absolute_prefix())

    def test_relative_prefix(self):

        lines = [
            ('tests/', 'tests/'),
            ('    /', None),
            ('var = "tests/dir/"', 'tests/dir/'),
            ('... /tmp/ tests/dir/', 'tests/dir/'),
        ]

        for (line, should) in lines:
            s = Scanner(line)
            
            self.assertEqual(should, s.get_relative_prefix())

    def test_mixed_prefix_and_basename(self):
        # (input, rel, abs, base)
        lines = [
            ('tests/', 'tests/', '/', None),
            ('    /he', None, '/', 'he'),
            ('var = "tests/dir/oi', 'tests/dir/', '/', 'oi'),
            ('... /tmp/ tests/dir/', 'tests/dir/', '/', None),
            ('... /tmp/ tests/dir/tmp/t', 'tests/dir/tmp/', '/tmp/', 't')
        ]

        for (line, should_rel, should_abs, should_base) in lines:
            s = Scanner(line)
            
            self.assertEqual(should_rel, s.get_relative_prefix())
            self.assertEqual(should_abs, s.get_absolute_prefix())
            self.assertEqual(should_base, s.get_basename())

    def test_smart_choose(self):
        # (input, rel, abs, base)
        lines = [
            ('tests/', 'tests/'),
            ('    /he', '/'),
            ('var = "tests/dir/oi', 'tests/dir/'),
            ('... /tmp/ tests/dir/', 'tests/dir/'),
            ('... /tmp/ tests/dir/tmp/t', 'tests/dir/tmp/')
        ]

        for (line, should) in lines:
            s = Scanner(line)

            s = Scanner(line)
            rel = s.get_relative_prefix()
            absolute = s.get_absolute_prefix()

            self.assertEqual(should, s.smart_choose(rel, absolute))

    def test_get_matching_dir_contents(self):

        lines = [
            ('tests/dir/', ['dev', 'heko', 'hello', 'tmp', 'verylong', 'hey', 'somefile']),
            ('tests/dir', ['dir']),
            ('    /c', ['etc', 'proc']),
            ('... /tmp/ tests/dir/h', ['heko', 'hello', 'hey'])
        ]

        for (line, should) in lines:
            s = Scanner(line)

            s = Scanner(line)
            rel = s.get_relative_prefix()
            absolute = s.get_absolute_prefix()
            basename = s.get_basename()

            p = s.smart_choose(rel, absolute)

            #print('looking for p: ' + p + ' in ' + os.getcwd())

            is_list = s._get_matching_dir_contents(p, basename)
            self.assertEqual(sorted(should), sorted(is_list))

    def test_get_comp_list(self):

        line, should = ('tests/dir/', [
            ('dev\tFC', 'dev'),
            ('heko\tFC', 'heko'),
            ('hello\tFC', 'hello'),
            ('tmp\tFC', 'tmp'),
            ('verylong\tFC', 'verylong'),
            ('hey\tFC', 'hey'),
            ('somefile\tFC', 'somefile')
        ])

        s = Scanner(line)

        self.assertEqual(sorted(should), sorted(s.get_comp_list()))




# coding=utf-8
import unittest
# from testCases.test_timer import timer_suite
# import HtmlTestRunner
'''suite = unittest.TestSuite(timer_suite)
runner = unittest.TextTestRunner()'''
test_dir = './testCases/'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
runner = unittest.TextTestRunner()
# HtmlTestRunner不会执行setUpClass tearDownClass
# runner = HtmlTestRunner.HTMLTestRunner(output='example_dir')
runner.run(discover)

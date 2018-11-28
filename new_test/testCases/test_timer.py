# coding=utf-8
from testHelper import Producer
import unittest
from COM import SerialTestRunner as STR
import time

valuedict = {
    'id': [i for i in range(2)],
    'trig_val': [1, 5],
}
formatdict = {
    'id': '%02d',
    'trig_val': '%d',

}


class Timer_start_stop(unittest.TestCase):
    cmd_pattern = 'timer_start_stop id'
    cmd_timer_int = 'timer_reload id'
    name_timer_int = 'test_timer_int_{:02d}'

    @classmethod
    def setUpClass(cls):
        # Producer.born_cases_from_demo(cls, valuedict, formatdict)
        print('setup class.............')
        cls.logfile = open('tmp.txt', 'w')
        cls.runner = STR.SerialRunner(cls.logfile)
        cls.runner.getport('COM39')
        STR.enter_menu(cls.runner, 'timer')

    @classmethod
    def tearDownClass(cls):
        cls.logfile.close()
        print('teardown class.............')

    @staticmethod
    def demo(self, cmd):
        print('running', cmd)
        # self.assertIn('0', cmd)
        res = self.runner.serialtest(cmd, [
            'decrease', 'pass'], ['fail'])
        if res[0] == 'Pass':
            self.assertTrue(True)
        if res[0] == 'Fail':
            self.assertTrue(False)

    @staticmethod
    def timer_int_demo(self, cmd):
        print('running', cmd)
        # self.assertIn('0', cmd)
        res = self.runner.serialtest(cmd, [
            'pass'], ['fail'])
        if res[0] == 'Pass':
            self.assertTrue(True)
        if res[0] == 'Fail':
            self.assertTrue(False)

    def setUp(self):
        print('>>>>>>>>>>')

    def tearDown(self):
        print('<<<<<<<<<<')

    @unittest.skip("test01_start_stop")
    def test01_start_stop(self):
        print('start_stop_test...')
        cmd = 'timer_start_stop id'
        cases = Producer.combine(cmd, valuedict, formatdict)
        for i in cases:
            print(i)
        self.assertTrue(False)


Producer.born_cases_from_demo(Timer_start_stop, valuedict, formatdict)
Producer.born_cases_from_demo(Timer_start_stop, valuedict, formatdict,
                              cmd_pattern=Timer_start_stop.cmd_timer_int,
                              name_pattern=Timer_start_stop.name_timer_int,
                              demo=Timer_start_stop.timer_int_demo)

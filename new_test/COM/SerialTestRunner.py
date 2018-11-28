# import SerialHelper as sh
import COM.SerialHelper as sh
import time
import logging
import re


class SerialRunner():

    def __init__(self, fileIns):
        self.logfile = fileIns

    def getport(self, *args, **kwargs):
        self.serialInstant = sh.SerialHelper(*args, **kwargs)
        self.serialInstant.start()

    def closeport(self):
        if self.serialInstant:
            self.serialInstant.stop

    def inputStr(self, strdata):
        self.serialInstant.write(strdata)

    def assert_from_keyword(self, log, passlist, faillist):
        '''
        if result get, pass or fail, return True,
        else return False
        '''
        passtxt = passlist[0]
        if any([i in log for i in faillist]):
            return True, 'Fail'
        for i in passlist[1:]:
            passtxt += r'[\w\W]*%s' % (i)
        # print(passtxt)
        pattern_pass = re.compile(passtxt)
        if pattern_pass.search(log):
            return True, 'Pass'
        return False,

    def assert_with_re(self, text, passtxt, failtxt):
        pattern_pass = re.compile(passtxt)
        pattern_fail = re.compile(failtxt)
        if pattern_fail.search(text):
            return True, ('Fail', 'Reason')
        if pattern_pass.search(text):
            return True, ('Pass', 'Pass')
        return False, ('noMatch', 'noMatch')

    def serTest(self, testfunc, *testfuncpara, sec_timeout=5):
        self.serialInstant.receive_data = ''
        time_start = time.time()
        timeout = True
        log_log = ''
        while self.serialInstant.alive and (time.time() - time_start < sec_timeout):
            try:
                self.serialInstant.read(500)
            except Exception as e:
                logging.error(e)
            result = testfunc(self.serialInstant.receive_data, *testfuncpara)
            # print(len(serialInstant.receive_data))
            log_log += self.serialInstant.receive_stamp
            # match found
            if result[0]:
                print(result[1])
                res = result[1]
                timeout = False
                break
        if timeout:
            res = 'Fail', 'Timeout {:d}'.format(sec_timeout)
        return res, log_log

    def serialtest(self, inputstr, passkws, failkws, tm=10):
        self.inputStr(inputstr + '\n')
        res, log = self.serTest(self.assert_from_keyword, passkws, failkws)
        if self.logfile:
            self.logfile.write(log)
        return res


def enter_menu(runnerInstant, name):
    runnerInstant.inputStr('q' + '\n')
    time.sleep(0.5)
    runnerInstant.inputStr(name + '\n')
    time.sleep(0.5)


if __name__ == '__main__':
    logfile = open('tmp.txt', 'w')
    runner = SerialRunner(logfile)
    runner.getport('COM39')
    enter_menu(runner, 'timer')
    runner.serialtest('timer_start_stop 0', ['decrease', 'pass'], ['fail'])
    logfile.close()

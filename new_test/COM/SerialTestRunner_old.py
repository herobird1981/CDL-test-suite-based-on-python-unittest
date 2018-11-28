# import SerialHelper as sh
import COM.SerialHelper as sh

import time
import logging
import re


def getport(*args, **kwargs):
    serialInstant = sh.SerialHelper(*args, **kwargs)
    serialInstant.start()
    return serialInstant


def inputStr(serialInstant, strdata):
    serialInstant.write(strdata)


def assert_from_keyword(log, passlist, faillist):
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


def assert_with_re(text, passtxt, failtxt):
    pattern_pass = re.compile(passtxt)
    pattern_fail = re.compile(failtxt)
    if pattern_fail.search(text):
        return True, ('Fail', 'Reason')
    if pattern_pass.search(text):
        return True, ('Pass', 'Pass')
    return False, ('noMatch', 'noMatch')


def serTest(serialInstant, testfunc, *testfuncpara, sec_timeout=5):
    serialInstant.receive_data = ''
    time_start = time.time()
    timeout = True
    log_log = ''
    while serialInstant.alive and (time.time() - time_start < sec_timeout):
        try:
            serialInstant.read(500)
        except Exception as e:
            logging.error(e)
        result = testfunc(serialInstant.receive_data, *testfuncpara)
        # print(len(serialInstant.receive_data))
        log_log += serialInstant.receive_stamp
        # match found
        if result[0]:
            # print(result[1])
            res = result[1]
            timeout = False
            break
    if timeout:
        res = 'Fail', 'Timeout {:d}'.format(sec_timeout)
        # print('timeout')
    return res, log_log


def serialtest(serialInstant, inputstr, passkws, failkws, tm=10):
    inputStr(serialInstant, inputstr + '\n')
    res, log = serTest(serialInstant, assert_from_keyword, passkws, failkws)
    open('tmp.txt', 'a').write(log)
    return res


if __name__ == '__main__':
    port = getport('COM39')
    inputStr(port, 'q\n')
    time.sleep(0.5)
    inputStr(port, 'timer\n')
    time.sleep(0.5)
    # inputStr(port, 'timer_start_stop 0\n')
    # log = serTest(port, assert_from_keyword, ['decrease', 'pass'], ['fail'])
    serialtest(port, 'timer_start_stop 0', ['decrease', 'pass'], ['fail'])
    # log = serTest(port, assert_with_re, r'pass', r'fail')
    # print(log)
    # print(port.receive_data)
    # print(get_time_stamp())

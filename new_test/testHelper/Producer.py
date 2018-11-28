# coding=utf-8
class Produce:

    def __init__(self, *args):
        '''
        args is a list of the parameter list
        such as [[1, 2, 4], ['a', 'b', 'c']]
        pick up a parameter from the every parameter list ,and return
        these parameters every iter
        such as [1, 'b'], [2, 'c']
        '''
        self.args = args
        self.arglen = len(args)
        self.current_indexs = [0 for arg in args]
        self.max_indexs = [len(arg) - 1 for arg in args]
        self.endflag = False

    def __next__(self):
        if self.endflag:
            raise StopIteration
        indexs = self.current_indexs[:]
        self.next_indexs()
        return [self.args[i][indexs[i]] for i in range(self.arglen)]

    def next(self):
        return self.__next__()

    def __iter__(self):
        return self

    def next_indexs(self):
        i = self.arglen - 1
        while i >= 0:
            if self.current_indexs[i] + 1 > self.max_indexs[i]:
                self.current_indexs[i] = 0
                i -= 1
            else:
                self.current_indexs[i] += 1
                break
        if i < 0:
            self.endflag = True

#################################################
#get command combination                      #
#################################################


class CMDiter:

    def __init__(self, valuedict, formatdict, cmd):
        self.valuedict = valuedict
        self.formatdict = formatdict
        self.cmd = cmd
        self.valuelist = []
        self.run()

    def __iter__(self):
        return self

    def __next__(self):
        paras = self.paraproductiter.next()
        return self.cmd_format % tuple(paras)

    def next(self):
        return self.__next__()

    def replacestr(self):
        oldlist = self.cmd.split()
        newlist = []
        valuelist = []
        newstr = ''
        for key in oldlist:
            if (key in self.formatdict) and (key in self.valuedict):
                str_fmt = self.formatdict[key]
                value = self.valuedict[key]
                valuelist.append(value)
            else:
                str_fmt = key
            newlist.append(str_fmt)
        newstr = ' '.join(newlist)
        self.cmd_format = newstr
        self.valuelist = valuelist

    def run(self):
        self.replacestr()
        self.paraproductiter = Produce(*self.valuelist)


def combine(cmd, valuedict, formatdict):
    return CMDiter(valuedict, formatdict, cmd)


def born_cases_from_demo(cls, valuedict=None, formatdict=None, cmd_pattern=None, name_pattern=None, demo=None):
    if not name_pattern:
        name_pattern = 'test_{:02d}' + cls.__name__
    if not demo:
        demo = cls.demo
    if not cmd_pattern:
        cmd_pattern = cls.cmd_pattern
    if not formatdict:
        formatdict = cls.formatdict
    if not valuedict:
        valuedict = cls.valuedict
    print(demo, 'lay eggs now...')
    cmds_iter = CMDiter(valuedict, formatdict, cmd_pattern)
    counter = 0
    for cmd in cmds_iter:
        def test(self, cmd=cmd):
            demo(self, cmd)
        setattr(cls, name_pattern.format(counter), test)
        counter += 1

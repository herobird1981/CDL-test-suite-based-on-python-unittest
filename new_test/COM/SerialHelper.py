import sys
import threading
import time
import serial
import binascii
import logging


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "[%s.%03d]" % (data_head, data_secs)
    return time_stamp


class SerialHelper():

    def __init__(self, Port="COM39", BaudRate=115200, ByteSize=8, Parity="N", Stopbits=1):
        '''
        初始化一些参数
        '''
        self.l_serial = None
        self.alive = False
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.thresholdValue = 64
        self.receive_data = ""
        self.receive_stamp = ''

    def start(self):
        '''
        开始，打开串口
        '''
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = self.baudrate
        self.l_serial.bytesize = self.bytesize
        self.l_serial.parity = self.parity
        self.l_serial.stopbits = self.stopbits
        self.l_serial.timeout = 2

        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
        except Exception as e:
            self.alive = False
            logging.error(e)

    def stop(self):
        '''
        结束，关闭串口
        '''
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()

    def read(self, mtimeout=100):
        '''
        循环读取串口发送的数据
        '''
        stamp_data = []
        raw_data = []
        time_start = time.time()
        try:
            while self.alive and (time.time() - time_start < mtimeout / 1000):
                # number = self.l_serial.inWaiting()
                # if number:
                #     self.receive_data += self.l_serial.read(
                #         number).decode()
                #     if self.thresholdValue <= len(self.receive_data):
                #         self.receive_data = ""
                read_data = self.l_serial.read_all().decode()
                if read_data:
                    raw_data.append(read_data)
                    stamp_data.append(read_data.replace(
                        '\r', '').replace('\n', '\n' + get_time_stamp()))
        except Exception as e:
            logging.error(e)
        finally:
            self.receive_stamp = ''.join(stamp_data)
            self.receive_data += ''.join(raw_data)

    def write(self, data, isHex=False):
        '''
        发送数据给串口设备
        '''
        if self.alive:
            # print('is alive\n')
            if self.l_serial.isOpen():
                if isHex:
                    # data = data.replace(" ", "").replace("\n", "")
                    data = binascii.unhexlify(data)
                self.l_serial.write(data.encode())
                # print('len:', len(data), len(data.encode()))

if __name__ == '__main__':
    # import threading
    # ser = SerialHelper()
    # ser.start()

    # ser.write("123", isHex=False)
    # thread_read = threading.Thread(target=ser.read)
    # thread_read.setDaemon(True)
    # thread_read.start()
    # import time
    # time.sleep(25)
    # ser.stop()
    ser = SerialHelper()
    ser.start()
    ser.write('timer\n')
    ser.read()
    print(ser.receive_data)
    ser.stop()

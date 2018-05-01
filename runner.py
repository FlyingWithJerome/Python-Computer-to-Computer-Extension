'''
runner.py

This is the runner class.
Runner executes the program
'''
import _pickle # bad, but necessary

import pickle
import random
import socket
import sys
import threading
import time

from collections import defaultdict

class RunnerError(Exception):
    pass

class Runner(object):

    def __init__(self, self_name="host1", program=None, metadata="metadata.txt"):

        self.__make_socket()
        self.__variable_pool = defaultdict(dict)
        self.__name = self_name
        self.__ip_table = dict()
        
        with open(metadata) as mtdata:
            for lines in mtdata:
                lines = lines.strip("\n")
                if ":" in lines:
                    [name, ip] = lines.split(":")
                    self.__ip_table[name] = ip.strip()

        if self_name == "host1":
            self.__synchronize("host2", serial=-1)
        else:
            self.__synchronize("host1", serial=-1)

        print(self_name, " SYNC OK")

        start = time.time()
        self.__run()

        print("{:.3f}".format(time.time()-start))


    def __make_socket(self):
        self.__socket_member = socket.socket(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        self.__socket_member.setblocking(False)
        self.__socket_member.bind(("", 2048))

    def __run(self):
        if self.__name == "host1":
            with open("sample_copy_1.py") as source:
                exec(source.read())
        else:
            with open("sample_copy_2.py") as source:
                exec(source.read())

    def __synchronize(self, host_name, serial=-1):
        while True:
            self.__socket_member.sendto(bytes(str(serial).encode("ascii")), (self.__ip_table[host_name], 2048))
            try:
                sig = self.__socket_member.recv(1000)
                if sig.decode() == str(serial):
                    return
            except BlockingIOError:
                pass
            time.sleep(.5)


    def sendto(self, host_name, variable_name, data):
        assert host_name in self.__ip_table, "You do have this host registered"

        print(host_name, variable_name, data)

        data_pickled = pickle.dumps((self.__name, variable_name, data))
        self.__socket_member.sendto(data_pickled, (self.__ip_table[host_name], 2048))


    def __recv_data(self, host_name, variable_name):
        event = self.__timeout_event
        while True:
            try:
                data = self.__socket_member.recv(1000)
                print("get a data")
                host, var_name, value = pickle.loads(data)
                print("received data", host, var_name, value)
                if host == host_name and var_name == variable_name:
                    print("get ONE!")
                    self.__variable_pool[host_name][variable_name] = value
                    return
            except (BlockingIOError, ValueError, _pickle.UnpicklingError):
                continue
            
            if event.is_set():
                del event
                raise RunnerError("Cannot get the data from {} in timeout".format(host_name))

    def synchronize(self, host_name, serial_num=-1):
        self.__synchronize(host_name, serial=serial_num)

    def broadcast(variable_name, data):
        if len(self.__ip_table) < 2:
            raise RunnerError("Does not have any target to braodcast")
        for name in self.__ip_table:
            if name != self.__name:
                self.sendto(name, variable_name, data)

    def getfrom_nonblock(self, host_name, variable_name) -> object:
        if host_name in self.__variable_pool and\
            variable_name in self.__variable_pool[host_name]:
            return self.__variable_pool[host_name][variable_name]
        else:
            return None

    def getfrom(self, host_name, variable_name, timeout=5) -> object:
        if host_name in self.__variable_pool and\
            variable_name in self.__variable_pool[host_name]:
            return self.__variable_pool[host_name][variable_name]

        else:
            self.__timeout_event = threading.Event()

            poller = threading.Thread(target=self.__recv_data, args=(host_name, variable_name))
            poller.start()
            poller.join(timeout=timeout)
            self.__timeout_event.set()

            if variable_name in self.__variable_pool[host_name]:
                return self.__variable_pool[host_name][variable_name]

    def __del__(self):
        '''
        release sockets here
        '''
        self.__socket_member.close()

if __name__ == "__main__":
    r = Runner(self_name=sys.argv[1])
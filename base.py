class Computer:
    """Computer."""
    def __init__(self):
        self.__iface = NetworkInterface()
        self.__all_program = {}
        self.add_program(Standart_Program())

    def add_program(self, srv):
        """Add new program."""
        self.all_program()[srv.name()] = srv.func
        srv.set_comp(self)

    def all_program(self):
        """Return all program."""
        return self.__all_program

    def iface(self):
        """Return network interface."""
        return self.__iface

    def ping(self, addr):
        """Send ping to address."""
        return self.iface().ping(addr)

    def def_func(self, src_ip, msg):
        """Define function"""
        program = msg["program"]
        method_str = msg["method"]
        params = msg["params"]
        return self.all_program()[program](src_ip, method_str, params)

    def call(self, addr, name, command, args=None):
        """Call command to address."""
        message = {
            "program" : name,
            "method" : command,
            "params" : args
        }
        if addr == "myself":
            return self.def_func(addr, message)
        return self.iface().call([addr, self.ip(), message])

    def back(self):
        """Return information from host."""
        msg = self.iface().back()
        if msg != "No message":
            return self.def_func(msg[1], msg[-1])

    def ip(self):
        """Return ip address"""
        return self.iface().addr


class Network:
    """Network represents net."""

    def __init__(self):
        self.__hosts = {}
        self.message_pool = {}

    def add_host(self, comp, addr):
        """Add host to net."""
        self.__hosts[addr] = comp
        comp.iface().setup(self, addr)
        self.message_pool[addr] = []

    def ping(self, src, dst):
        """Ping sends ping to host."""
        if dst in self.__hosts:
            return f"ping from {src} to {dst}"
        return "Unknown host"

    def add_message_to_pool(self, msg):
        """Add merssage to host in message pool"""
        try:
            self.message_pool[msg[0]].append(msg)
        except KeyError:
            return "Unknown host"
        if msg[0] in self.__hosts:
            ans = self.__hosts[msg[0]].back()
            self.message_pool[msg[0]].pop()
            return ans
        return "Message added in pool"

    def number_hosts(self):
        """Return number of host"""
        return len(self.__hosts)

    def message_to(self, addr):
        """Check amount message to host"""
        return len(self.message_pool[addr])


class NetworkInterface:
    """Network interface."""

    def __init__(self):
        self.net = None
        self.addr = None

    def setup(self, net, addr):
        """Set net and address to interface."""
        self.net = net
        self.addr = addr

    def ping(self, addr):
        """Send ping to address."""
        if not self.net:
            return "No network"
        return self.net.ping(self.addr, addr)

    def call(self, msg : list):
        """Send Data to address."""
        if not self.net:
            return "No network"
        return self.net.add_message_to_pool(msg)

    def back(self):
        """Return information from host."""
        if not self.net:
            return "No network"
        if self.net.message_to(self.addr) > 0:
            message = self.net.message_pool[self.addr][-1]
            return message
        return "No message"


class Program:
    def __init__(self) -> None:
        self.__comp = None

    def set_comp(self, comp):
        """Set Computer"""
        self.__comp = comp

    def comp(self):
        """Return Computer"""
        return self.__comp


class Standart_Program(Program):

    @staticmethod
    def name():
        """Return Program name"""
        return "Standart_Program"

    def func(self, src_ip, command, args = None):
        """Define function"""
        if command == "receive_message":
            return self.receive_message(src_ip, args)
        return "Error"

    def receive_message(self, src_ip, params):
        """Method receive message from host"""
        return f"Data from {src_ip} has been received."

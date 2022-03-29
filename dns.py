from base import Program


class Record:
    """Single DNS record."""

    def __init__(self, name, addr):
        self.__name = name
        self.__addr = addr

    def get_name(self):
        """Return record name"""
        return self.__name

    def get_addr(self):
        """Return record addr"""
        return self.__addr


class DnsDb:
    """DNS database."""

    def __init__(self):
        self.__records = {}
        self.__addrs = {}

    def num_records(self):
        """Return number of records."""
        return len(self.__records)

    def add_record(self, record):
        """Add record."""
        self.__check_record(record)
        self.__records[record.get_name()] = record

    def resolve(self, name):
        """Return IP address by name."""
        try:
            return self.__records[name].get_addr()
        except KeyError:
            return None

    def __check_record(self, record):
        """Check for Duplicated address"""
        if record.get_addr() in self.__addrs:
            raise ValueError("Duplicated address")
        self.__addrs[record.get_addr()] = True


class DNS(Program):
    def __init__(self):
        super().__init__()
        self.__local_db = None
        self.__dns = None

    @staticmethod
    def name():
        """Return Program name"""
        return "DNS"

    def func(self, src_ip, command, args = None):
        """Define function"""
        if command == "resolve_non_rec":
            return self.resolveNonRecursive(src_ip, args)
        commands = {
        "resolve" : self.resolve,
        "set_dns" : self.set_dns_server,
        "set_db" : self.set_dns_db
        }
        try:
            return commands[command](args)
        except:
            return "Error"

    def resolve(self, name):
        """Recursive resolve addr"""
        ans = self.check_in_local_db(name)
        if not ans:
            if self.dns():
                if not self.comp().iface().net:
                    return None
                ans = self.comp().call(self.dns(), "DNS", "resolve", name)

        return ans

    def resolveNonRecursive(self,src_ip, name):
        """Non-Recursive resolve addr"""
        ans = self.check_in_local_db(name)
        if ans:
            return [ans, "IP"]

        if self.dns():
            if src_ip != "myself":
                return [self.dns(), "DNS"]

        ans = self.comp().call(self.dns(), "DNS", "resolve_non_rec", name)
        if ans:
            if ans[-1] == "IP":
                return ans[0]
            if ans[-1] == "DNS":
                addr = self.comp().call(ans[0], "DNS", "resolve_non_rec", name)
                return addr[0]
        return ans

    def set_dns_server(self, addr):
        """Set DNS server"""
        self.__dns = addr

    def set_dns_db(self, db):
        """Set DNS-DataBase"""
        self.__local_db = db

    def local_db(self):
        """Return local DNS DataBase"""
        return self.__local_db

    def dns(self):
        """Return IP DNS-server"""
        return self.__dns

    def check_in_local_db(self, name):
        """Check IP in local DNS-DataBase"""
        if self.local_db():
            return self.local_db().resolve(name)
        return None

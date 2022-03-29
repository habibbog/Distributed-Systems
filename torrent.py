from base import Program


class Torrent_File:
    def __init__(self):
        self.__file_name = None
        self.__file_size = None
        self.__number_shards = None
        self.__ip_seed = None

    def get_file_name(self):
        """Return file name"""
        return self.__file_name

    def get_file_size(self):
        """Return file size"""
        return self.__file_size

    def get_number_shards(self):
        """Return shards number"""
        return self.__number_shards

    def get_ip_seed(self):
        """Return IP seed"""
        return self.__ip_seed

    def set_file_name(self, name):
        """Set file name"""
        self.__file_name = name

    def set_file_size(self, size):
        """Set file size"""
        self.__file_size = size

    def set_number_shards(self, number_shards):
        """Set shards number"""
        self.__number_shards = number_shards

    def set_ip_seed(self, ip_seed):
        """Set IP seed"""
        self.__ip_seed = ip_seed


class TORRENT(Program):
    def __init__(self) -> None:
        super().__init__()
        self.__files = {}
        self.__torrent_files = {}

    def files(self):
        """Return files in Computer"""
        return self.__files

    def torrent_files(self):
        """Return Torrent files in Computer"""
        return self.__torrent_files

    @staticmethod
    def name():
        return "TORRENT"

    def func(self, src_ip, command, args = None):
        c1 = {
        "all_torrent_files" : self.torrent_files,
        "all_files" : self.files
        }
        c2 = {
        "get_torrent_file" : self.get_torrent_file,
        "create_torrent_file" : self.create_torrent_file,
        "seed" : self.seed_data,
        "download_torrent_file" : self.download_torrent_file,
        "download_file" : self.download_file,
        "get_shard" : self.get_shard
        }
        if command in c1.keys():
            return c1[command]()
        elif command in c2.keys():
            return c2[command](args)
        return "Error"

    def get_torrent_file(self, name):
        """Return Torrent file by name"""
        try:
            return self.torrent_files()[name]
        except:
            return "No torrent file"

    def create_torrent_file(self, data):
        """Create Torrent file by name"""
        torrent_file = Torrent_File()
        torrent_file.set_ip_seed(data["addr"])
        data = data["data"]
        torrent_file.set_file_name(data["file_name"])
        torrent_file.set_file_size(data["file_size"])
        try:
            torrent_file.set_number_shards(data["number_shards"])
        except:
            torrent_file.set_number_shards(len(data["shards"]))
        self.torrent_files()[data["file_name"]] = torrent_file
        return "Torrent file created"

    def seed_data(self, data):
        """Seed file"""
        tracker_ip = data["tracker_ip"]
        data = data["data"]

        params = {
            "addr" : self.comp().ip(),
            "data" : data
        }
        if self.comp().ping(tracker_ip) not in ("No network", "Unknown host"):
            ans = self.comp().call(tracker_ip, "TORRENT", "create_torrent_file", params)
            self.files()[data["file_name"]] = data["shards"]
            return ans
        return self.comp().ping(tracker_ip)

    def download_torrent_file(self, data):
        """Download Torrent file by name"""
        tracker_ip = data["tracker_ip"]
        file_name = data["name"]
        return self.comp().call(tracker_ip, "TORRENT", "get_torrent_file", file_name)

    def download_file(self, data):
        """Return file by name"""
        file_name = data["name"]
        torrent_file = self.download_torrent_file(data)
        if torrent_file != "No torrent file":
            ip_seed = torrent_file.get_ip_seed()
            number_shards = torrent_file.get_number_shards()
            self.files()[file_name] = [0 for _ in range(number_shards)]
            for i in range (number_shards):
                shard = self.download_shard(ip_seed, file_name, i)
                if shard not in ("No network", "Unknown host", "No file"):
                    self.files()[file_name][i] = shard
            return "File saved"
        return "The file is not distributed"

    def download_shard(self, ip_seed, file_name, i):
        """Return shard by index"""
        params = {
            "name" : file_name,
            "id" : i
        }
        return self.comp().call(ip_seed, "TORRENT", "get_shard", params)

    def get_shard(self, data):
        """Return shard by index"""
        file_name = data["name"]
        shard_number = data["id"]
        if file_name in self.files().keys():
            return self.files()[file_name][shard_number]
        return "No file"

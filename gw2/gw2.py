from os import path
import re
import requests


class Gw2:

    ACHI_DICT = {}  # name, id
    ACHI_DICT_CACHE = "gw2/achievements.txt"

    def __init__(self):
        pass

    # cache achievements
    def update_achi_dict(self):

        # skip if achievements already cached
        if path.exists(self.ACHI_DICT_CACHE):
            return

        # achievement pages are 0 % 76
        for page_nr in range(77):

            # api-endpoint
            URL = "https://api.guildwars2.com/v2/achievements"

            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'page': str(page_nr)}

            # sending get request and saving the response as response object
            r = requests.get(url=URL, params=PARAMS)

            # extracting data in json format
            data = r.json()

            for i in data:
                id = str(i["id"])
                name = str(i["name"])
                self.ACHI_DICT[name] = id

        # Store dict in a file
        f = open(self.ACHI_DICT_CACHE, "w")
        for entry in self.ACHI_DICT:
            f.write(entry + "->" + self.ACHI_DICT[entry] + "\n")
        f.close()

    # entry = 'Wurm Slayer'  self.ACHI_DICT[entry] = '52'

    def show_achi(self):
        for entry in self.ACHI_DICT:
            print(entry + " --> " + self.ACHI_DICT[entry])

    def load_achi_dict(self, path=""):
        if path == "":
            path = self.ACHI_DICT_CACHE

        file = open(path, 'r')
        Lines = file.readlines()

        for line in Lines:
            line = line.strip()
            line = line.split("->")
            name = line[0]
            id = line[1]
            self.ACHI_DICT[name] = id

    # If regex is false, get_id will return a string with the id
    # If regex is true, get_id will return a dict [name:id] for all entries that match the regex
    def get_id(self, achi_name, regex=False):
        # Returns a string
        if regex == False:
            return self.ACHI_DICT[achi_name]

        # Returns a dict
        ret = {}
        for entry in self.ACHI_DICT:
            found = re.search(achi_name, entry)
            if found:
                name = entry
                id = self.ACHI_DICT[entry]
                ret[name] = id

        return ret

    # Returns the full name of the achi with the specified id
    def get_name(self, achi_id):
        for entry in self.ACHI_DICT:
            name = entry
            id = self.ACHI_DICT[entry]
            if id == achi_id:
                return name

    def get_dailies(self, tier="T4"):
        # Prepare
        if tier[0] == "T":
            tier = "Daily Tier " + tier[-1]
        elif tier.lower() == "recommended":
            tier = "Recommended"
        else:
            print("Bad Format")
            return False

        # Use the gw2 api to get the dailies
        URL = "https://api.guildwars2.com/v2/achievements/daily"
        r = requests.get(url=URL)
        data = r.json()

        # Get the ids of the specified tier
        self.load_achi_dict()

        ret = []

        fractals = data["fractals"]
        for fractal in fractals:
            id = fractal["id"]
            name = self.get_name(str(id))

            if tier in name:
                ret.append(name)

        return ret

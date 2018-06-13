import feedparser
import json
import requests

class mal_crawler():
    def __init__(self):
        pass

    def malc0de(self):
        data_list = []
        d = feedparser.parse("http://malc0de.com/rss/")
        for mal in d['entries']:
            data_list.append({"url":mal['summary'].split(",")[0][5:],
                              "md5":mal['summary'].split(",")[4][6:]})
        return data_list

    def vxvault(self):
        data = requests.get("http://vxvault.net/URL_List.php").text.split("\r\n")
        for i in range(4):
            data.pop(0)
        return data

    def dasmalwerk(self):
        data_list = []
        data = json.loads(requests.get("http://dasmalwerk.eu/dasmalwerk.json").text)
        for i in data['items']:
            if not "debug" in i:
                url = "http://dasmalwerk.eu/zippedMalware/" + i['Filename'] + ".zip"
                data_list.append({"url":url, "sha256":i['Hashvalue'],"filename":i['Filename']})
        return data_list

    def malshare(self):
        data_list = []
        api_key = "7016c44e7fada5a7cfd4f558b0f2e4610a65460629a3dfe0168be8d9e8472601"
        hashes = json.loads(requests.get("http://api.malshare.com/api.php?api_key="+api_key+"&action=getlist").text)
        for hash_ in hashes:
            data_list.append({"url":"http://api.malshare.com/api.php?api_key=" + 
                              api_key + "&action=getfile&hash=" + hash_['md5'], 
                              "md5": hash_['md5']})
        return data_list

    def urlhaus(self):
        data_list = []
        data = requests.get("https://urlhaus.abuse.ch/downloads/csv/").text.split("\r\n")
        for i in range(9):
            data.pop(0)

        for i in data:    
            split_data = i.split(",")
            try:
                if split_data[3][1:-1] == "online":
                    url = i.split(",")[2][1:-1]
                    list2 = [x for x in url.split("/") if x != ""]
                    filename = list2[-1]
                    data_list.append({"url":url, 
                                    "filename":filename})
            except:
                pass
        return data_list

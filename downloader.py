from crawler import *
import urllib
import os
import logging
import requests
import hashlib
import zipfile

a = mal_crawler()
current_path = os.path.dirname(os.path.realpath(__file__))
name = input("input : ")

def check_http_string(data):
    if not "http://" in data:
        data = "http://"+data
    return data

if name == "malc0de":
    if not os.path.exists("malc0de"):
        os.makedirs("malc0de")
        print("Create Dir malc0de")

    malc0de = a.malc0de()
    for data in malc0de:
        url = check_http_string(data['url'])
        
        try:
            urllib.request.urlretrieve(url, current_path + "\\malc0de\\" + data['md5'])

        except urllib.error.HTTPError:
            pass

        except urllib.error.URLError:
            print("URLError : " + data['url'])

elif name == "malshare":
    if not os.path.exists("malshare"):
        os.makedirs("malshare")
        print("Create Dir malshare")

    malshare = a.malshare()
    for data in malshare:
        url = check_http_string(data['url'])
        urllib.request.urlretrieve(url, current_path + "\\malshare\\" + data['md5'])

elif name == "vxvault":
    if not os.path.exists("vxvault"):
        os.makedirs("vxvault")
        print("Create Dir vxvault")

    vxvault = a.vxvault()
    for url in vxvault:
        url = check_http_string(url)
        try:
            urllib.request.urlretrieve(url, current_path + "\\vxvault\\malshare_samples")
            f = open(current_path + "\\vxvault\\malshare_samples", "rb")
            data = f.read()
            f.close()

            os.rename(current_path + "\\vxvault\\malshare_samples", 
                      current_path + "\\vxvault\\" + hashlib.md5(data).hexdigest())
        except urllib.error.URLError:
            print("URLError : " + url)
            pass
            
        except FileExistsError:
            os.remove(current_path + "\\vxvault\\malshare_samples")
            print("FileExistsError : " + url)

elif name == "dasmalwerk":
    if not os.path.exists("dasmalwerk"):
        os.makedirs("dasmalwerk")
        print("Create Dir dasmalwerk")

    dasmalwerk = a.dasmalwerk()
    for data in dasmalwerk:
        urllib.request.urlretrieve(data['url'], 
                                   current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
        Zip = zipfile.ZipFile(current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
        Zip.setpassword(pwd=b"infected")
        Zip.extractall(current_path + "\\dasmalwerk\\")
        Zip.close()

        os.remove(current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
        os.rename(current_path + "\\dasmalwerk\\" + data['filename'], 
                  current_path + "\\dasmalwerk\\" + data['sha256'])

        



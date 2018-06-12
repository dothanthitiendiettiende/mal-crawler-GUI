# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt-designer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from crawler import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import urllib
import hashlib
import zipfile
import sqlite3
import time
import yara
import sys

# import multiprocessing
import threading

a = mal_crawler()
current_path = os.path.dirname(os.path.realpath(__file__))

def check_http_string(data):
    if not data.startswith("http://"):
        data = "http://"+data
    return data

class Ui_Dialog(object):
    def __init__(self):
        self.t1 = threading.Thread(target=self.malc0de_download)
        self.t2 = threading.Thread(target=self.malshare_download)
        self.t3 = threading.Thread(target=self.vxvault_download)
        self.t4 = threading.Thread(target=self.dasmalwerk_download)

        self.malc0de_data = []
        self.malshare_data = []
        self.vxvault_data = []
        self.dasmalwerk_data = []

        try:
            self.rule = yara.compile(source= open("rule.yar","r").read())

        except FileNotFoundError:
            print ("File not found")
            sys.exit()

        except yara.SyntaxError:
            print ("SyntaxError")
            sys.exit()

    def malc0de_download(self):
        count = 0
        if not os.path.exists("malc0de"):
            os.makedirs("malc0de")
            print("Create Dir malc0de")
        malc0de = a.malc0de()
        for data in malc0de:

            if count < self.spinBox_3.value():
                url = check_http_string(data['url'])
                    
                try:
                    urllib.request.urlretrieve(url, current_path + "\\malc0de\\" + data['md5'])
                    f = open(current_path + "\\malc0de\\" + data['md5'], "rb")
                    b = f.read()
                    matches = self.rule.match(data=b)
                    match_result = []

                    try:
                        for match in matches:
                            match_result.append(match.strings[0][1])
                    except IndexError:
                        match_result = []

                    self.malc0de_data.append([time.strftime("%Y-%m-%d"), url, hashlib.md5(b).hexdigest(), "", ','.join(match_result)])
                    self.malc0de_setText()
                    f.close()
                    count += 1

                except urllib.error.HTTPError:
                    pass

                except urllib.error.URLError:
                    print("URLError : " + data['url'])

            else:
                break


    def malc0de_threading(self):
        if self.t1.isAlive():
            print ("This Thread is Alive")
        else:
            self.t1.start()

    def malshare_download(self):
        count = 0
        if not os.path.exists("malshare"):
            os.makedirs("malshare")
            print("Create Dir malshare")
        malshare = a.malshare()
        for data in malshare:
            if count < self.spinBox.value():
                url = check_http_string(data['url'])
                urllib.request.urlretrieve(url, current_path + "\\malshare\\" + data['md5'])

                f = open(current_path + "\\malshare\\" + data['md5'], "rb")
                b = f.read()
                matches = self.rule.match(data=b)
                match_result = []

                try:
                    for match in matches:
                        match_result.append(match.strings[0][1])
                except IndexError:
                    match_result = []

                self.malshare_data.append([time.strftime("%Y-%m-%d"), url, hashlib.md5(b).hexdigest(), "", ','.join(match_result)])
                self.malshare_setText()
                f.close()
                count += 1
            else:
                break


    def malshare_threading(self):
        if self.t2.isAlive():
            print ("This Thread is Alive")
        else:
            self.t2.start()

    def vxvault_download(self):
        count = 0
        if not os.path.exists("vxvault"):
            os.makedirs("vxvault")
            print("Create Dir vxvault")
        vxvault = a.vxvault()
        for url in vxvault:
            if count < self.spinBox_2.value():
                url = check_http_string(url)
                try:
                    urllib.request.urlretrieve(url, current_path + "\\vxvault\\malshare_samples")
                    f = open(current_path + "\\vxvault\\malshare_samples", "rb")
                    hash_ = hashlib.md5(f.read()).hexdigest()
                    f.close()

                    os.rename(current_path + "\\vxvault\\malshare_samples", 
                            current_path + "\\vxvault\\" + hash_)

                    f = open(current_path + "\\vxvault\\" + hash_, "rb")
                    matches = self.rule.match(data=f.read())
                    match_result = []
                    
                    try:
                        for match in matches:
                            match_result.append(match.strings[0][1])
                    except IndexError:
                        match_result = []

                    self.vxvault_data.append([time.strftime("%Y-%m-%d"), url, hash_, "", ','.join(match_result)])
                    self.vxvault_setText()
                    f.close()
                    count += 1

                except urllib.error.URLError:
                    print("URLError : " + url)
                    pass
                        
                except FileExistsError:
                    os.remove(current_path + "\\vxvault\\malshare_samples")
                    print("FileExistsError : " + url)

            else:
                break


    def vxvault_threading(self):
        if self.t3.isAlive():
            print ("This Thread is Alive")
        else:
            self.t3.start()

    def dasmalwerk_download(self):
        count = 0
        if not os.path.exists("dasmalwerk"):
            os.makedirs("dasmalwerk")
            print("Create Dir dasmalwerk")
        dasmalwerk = a.dasmalwerk()
        for data in dasmalwerk:
            if count < self.spinBox_4.value():
                urllib.request.urlretrieve(data['url'], 
                                        current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
                Zip = zipfile.ZipFile(current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
                Zip.setpassword(pwd=b"infected")
                Zip.extractall(current_path + "\\dasmalwerk\\")
                Zip.close()

                os.remove(current_path + "\\dasmalwerk\\" + data['sha256'] + ".zip")
                f = open(current_path + "\\dasmalwerk\\" + data['filename'], "rb")
                hash_ = hashlib.md5(f.read()).hexdigest()
                f.close()
                try:
                    os.rename(current_path + "\\dasmalwerk\\" + data['filename'], 
                            current_path + "\\dasmalwerk\\" + hash_)

                    f = open(current_path + "\\dasmalwerk\\" + hash_, "rb")
                    b = f.read()
                    matches = self.rule.match(data=b)
                    match_result = []
                    
                    try:
                        for match in matches:
                            match_result.append(match.strings[0][1])
                    except IndexError:
                        match_result = []

                    self.dasmalwerk_data.append([time.strftime("%Y-%m-%d"), data['url'], hash_, "", ','.join(match_result)])
                    self.dasmalwerk_setText()
                    count += 1
                except FileExistsError:
                    print ("FIleExistsError")
                    os.remove(current_path + "\\dasmalwerk\\" + data['filename'])
            else:
                break
        
    
    def dasmalwerk_threading(self):
        if self.t4.isAlive():
            print ("This Thread is Alive")
        else:
            self.t4.start()

    def malc0de_setText(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget.setRowCount(len(self.malc0de_data))

        for i in range(len(self.malc0de_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 4, item)

        for idx, i in enumerate(self.malc0de_data):
            item = self.tableWidget.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

    def malshare_setText(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget_2.setRowCount(len(self.malshare_data))

        for i in range(len(self.malshare_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setVerticalHeaderItem(i, item)
            item = self.tableWidget_2.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))

        for i in range(len(self.malshare_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 4, item)

        for idx, i in enumerate(self.malshare_data):
            item = self.tableWidget_2.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_2.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_2.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_2.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_2.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

    def vxvault_setText(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget_3.setRowCount(len(self.vxvault_data))

        for i in range(len(self.vxvault_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setVerticalHeaderItem(i, item)
            item = self.tableWidget_3.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 4, item)

        for idx, i in enumerate(self.vxvault_data):
            item = self.tableWidget_3.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_3.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_3.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_3.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_3.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

    def dasmalwerk_setText(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget_4.setRowCount(len(self.dasmalwerk_data))

        for i in range(len(self.dasmalwerk_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setVerticalHeaderItem(i, item)
            item = self.tableWidget_4.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 4, item)

        for idx, i in enumerate(self.dasmalwerk_data):
            item = self.tableWidget_4.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_4.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_4.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_4.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_4.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

    def modify_rule(self):
        try:
            self.rule = yara.compile(source= self.plainTextEdit_2.toPlainText())
            f = open("rule.yar","w")
            f.write(self.plainTextEdit_2.toPlainText())
            f.close()
        except yara.SyntaxError:
            print ("syntax error")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(838, 794)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TabWidget1 = QtWidgets.QTabWidget(Dialog)
        self.TabWidget1.setObjectName("TabWidget1")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.gridLayout.setSpacing(30)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setMouseTracking(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 3, 1, 1)        
        self.pushButton_3 = QtWidgets.QPushButton(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setMouseTracking(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setMouseTracking(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab1)
        self.pushButton.setBaseSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setMouseTracking(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.tab1)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinBox_4.setFont(font)
        self.spinBox_4.setMouseTracking(False)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout.addWidget(self.spinBox_4, 3, 3, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.tab1)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setMouseTracking(False)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 3, 2, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.tab1)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinBox.setFont(font)
        self.spinBox.setMouseTracking(False)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 3, 1, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.tab1)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setMouseTracking(False)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.label_2 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tabWidget = QtWidgets.QTabWidget(self.tab1)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 761, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(self.malc0de_data))

        for i in range(len(self.malc0de_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()

        for i in range(len(self.malc0de_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(0, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(0, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(0, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(0, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(0, 4, item)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 10, 761, 211))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(len(self.malshare_data))

        for i in range(len(self.malshare_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setVerticalHeaderItem(i, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)

        for i in range(len(self.malshare_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setItem(i, 4, item)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 10, 761, 211))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setRowCount(len(self.vxvault_data))

        for i in range(len(self.vxvault_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setVerticalHeaderItem(i, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, item)

        for i in range(len(self.vxvault_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_3.setItem(i, 4, item)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_4.setGeometry(QtCore.QRect(10, 10, 761, 211))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(5)
        self.tableWidget_4.setRowCount(len(self.dasmalwerk_data))

        for i in range(len(self.dasmalwerk_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setVerticalHeaderItem(i, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(4, item)

        for i in range(len(self.dasmalwerk_data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_4.setItem(i, 4, item)

        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab1)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.TabWidget1.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.tab2)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        
        try:
            f = open("rule.yar","r")
            self.plainTextEdit_2.insertPlainText(f.read())
            f.close()
        except:
            print ("Not Found rule.yar")
            pass

        self.gridLayout_3.addWidget(self.plainTextEdit_2, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.modify_rule)
        self.gridLayout_3.addWidget(self.pushButton_5, 2, 0, 1, 1)
        self.TabWidget1.addTab(self.tab2, "")
        self.gridLayout_2.addWidget(self.TabWidget1, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.TabWidget1.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_4.setText(_translate("Dialog", "dasmalwerk"))
        self.pushButton_4.clicked.connect(self.dasmalwerk_threading)
        self.pushButton_3.setText(_translate("Dialog", "vxvault"))
        self.pushButton_3.clicked.connect(self.vxvault_threading)
        self.pushButton_2.setText(_translate("Dialog", "malshare"))
        self.pushButton_2.clicked.connect(self.malshare_threading)
        self.pushButton.setText(_translate("Dialog", "malc0de"))
        self.pushButton.clicked.connect(self.malc0de_threading)
        self.label_2.setText(_translate("Dialog", "Sample Database"))

        for i in range(len(self.malc0de_data)):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Timestamp"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "URL"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "MD5"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Virustotal"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Yara Match"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        for idx, i in enumerate(self.malc0de_data):
            item = self.tableWidget.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "malc0de"))
        
        for i in range(len(self.malc0de_data)):
            item = self.tableWidget_2.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))

        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Timestamp"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "URL"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "MD5"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Virustotal"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Yara Match"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)

        for idx, i in enumerate(self.malshare_data):
            item = self.tableWidget_2.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_2.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_2.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_2.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_2.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "malshare"))
        
        for i in range(len(self.vxvault_data)):
            item = self.tableWidget_3.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))

        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Timestamp"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "URL"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "MD5"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Virustotal"))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Yara Match"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)

        for idx, i in enumerate(self.vxvault_data):
            item = self.tableWidget_3.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_3.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_3.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_3.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_3.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "vxvault"))
        
        for i in range(len(self.dasmalwerk_data)):
            item = self.tableWidget_4.verticalHeaderItem(i)
            item.setText(_translate("Dialog", str(i+1)))

        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Timestamp"))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "URL"))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "MD5"))
        item = self.tableWidget_4.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Virustotal"))
        item = self.tableWidget_4.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Yara Match"))
        __sortingEnabled = self.tableWidget_4.isSortingEnabled()
        self.tableWidget_4.setSortingEnabled(False)

        for idx, i in enumerate(self.dasmalwerk_data):
            item = self.tableWidget_4.item(idx, 0)
            item.setText(_translate("Dialog", i[0]))
            item = self.tableWidget_4.item(idx, 1)
            item.setText(_translate("Dialog", i[1]))
            item = self.tableWidget_4.item(idx, 2)
            item.setText(_translate("Dialog", i[2]))
            item = self.tableWidget_4.item(idx, 3)
            item.setText(_translate("Dialog", i[3]))
            item = self.tableWidget_4.item(idx, 4)
            item.setText(_translate("Dialog", i[4]))

        self.tableWidget_4.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "dasmalwerk"))
        self.label.setText(_translate("Dialog", "Log"))
        self.TabWidget1.setTabText(self.TabWidget1.indexOf(self.tab1), _translate("Dialog", "Mal-Crawler"))
        self.label_3.setText(_translate("Dialog", "Yara Rule Editor"))
        self.pushButton_5.setText(_translate("Dialog", "Save"))
        self.TabWidget1.setTabText(self.TabWidget1.indexOf(self.tab2), _translate("Dialog", "Yara Rule Editor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


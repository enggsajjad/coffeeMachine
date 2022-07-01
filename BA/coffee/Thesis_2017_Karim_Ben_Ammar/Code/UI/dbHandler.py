#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys
import urllib.request
from datetime import datetime
from serverCommunication import passOrder

def fetcUsersWithUID():
    req = urllib.request.urlopen("http://i80misc01.ira.uka.de/coffee/getusers.php?secret=42!")
    response = req.read().decode('utf-8')
    response = response.replace(' ', '').split('\n')
    temp = list(map(lambda x : x.split(';')[:3], response))
    return temp

def fetcUsersWithBalance():
    req = urllib.request.urlopen("http://i80misc01.ira.uka.de/coffee/userz.php")
    response = req.read().decode('ISO-8859-1')
    response = response.replace(' ', '').split('\n')[1:]
    temp = list(map(lambda x : x.split(',')[:3], response))
    return temp

def prepareData():
    usersUID = fetcUsersWithUID()
    usersBalance = fetcUsersWithBalance()
    users = []
    for uid in usersUID:
        if uid:
         for balance in usersBalance:
             if balance:
                 if uid[0] == balance[0]:
                    in_first = set(uid)
                    in_second = set(balance)
                    in_second_but_not_in_first = in_second - in_first
                    users.append(uid + list(in_second_but_not_in_first))
    return users

def updateDB():
    users = prepareData()
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try :
        cur = conn.cursor()
        sql = "TRUNCATE `users`"
        cur.execute(sql)
        for user in users:
            if not len(user) < 4 :
                sql = "INSERT INTO `users` (`uid`, `username`, `balance`) VALUES (%s, %s, %s)"
                cur.execute(sql, (user[2], user[1], user[3]))
        conn.commit()
    finally:
        conn.close()

def getMilkChoice(uid):
    decimalUID = int(uid, 16)
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try:
        cur = conn.cursor()
        sql = "SELECT `milk` FROM `milk_choice` WHERE `uid`=%s"
        cur.execute(sql, (decimalUID,))
        result = cur.fetchone()
        return result
    finally:
        conn.close()

def setMilkChoice(uid, choice):
    decimalUID = int(uid, 16)
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try:
        cur = conn.cursor()
        sql = "INSERT INTO `milk_choice` (`uid`, `milk`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `milk`=%s"
        cur.execute(sql, (decimalUID, choice, choice))
        conn.commit()
    finally:
        conn.close()

def getUser(uid):
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try :
        cur = conn.cursor()
        sql = "SELECT `username`, `balance`, `limit_per_day`, `limit_per_month` FROM `users` WHERE `uid`=%s"
        cur.execute(sql, (uid,))
        result = cur.fetchone()
        return result
    finally:
        conn.close()

def updateUser(uid, balance, limit_per_day, limit_per_month):
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try :
        cur = conn.cursor()
        sql = "UPDATE `users` set `balance`=%s, `limit_per_day`=%s, `limit_per_month`=%s WHERE `uid`=%s"
        cur.execute(sql, (balance, limit_per_day, limit_per_month, uid))
        conn.commit()
    finally:
        conn.close()

def addOfflineTransaction(uid, product, milk):
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cur = conn.cursor()
        sql = "INSERT INTO `transactions` (`uid`, `product`, `milk`, `time`) VALUES(%s, %s, %s, %s)"
        cur.execute(sql, (uid, product, milk, time))
        conn.commit()
    finally:
        conn.close()

def handleOfflineTransactions():
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='coffee_time')
    try :
        cur = conn.cursor()
        sql = "SELECT * FROM `transactions`"
        cur.execute(sql)
        transactions = cur.fetchall()
        if transactions :
            for transaction in transactions :
                passOrder(transaction[1], transaction[2], transaction[3])
            sql = "TRUNCATE transactions"
            cur.execute(sql)
            conn.commit()
    finally:
        conn.close()

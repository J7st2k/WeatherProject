import requests
import re
import os
import psycopg2
from bs4 import BeautifulSoup
import datetime
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QListWidgetItem, QListWidget, QSizePolicy, QComboBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import asyncio
import json
from qasync import QEventLoop


def get1htime():
    now = datetime.datetime.now().hour
    time_travel = now + 1
    esteer = ''
    while time_travel % 24 != now:
        input = ''
        if time_travel % 24 < 10:
            input = '0'
        input = input + f'{time_travel % 24}'+':00'
        esteer = esteer + f'{input:6}'
        time_travel = time_travel + 1
    input = ''
    if time_travel % 24 < 10:
        input = '0'
    input = input + f'{time_travel % 24}'+':00'
    esteer = esteer + f'{input:6}'
    return esteer


def get3htime():
    now = datetime.datetime.now().hour
    time_travel = 1
    while time_travel <= now:
        time_travel = time_travel + 3
    time_travel = time_travel % 24
    now = time_travel - 3
    esteer = ''
    while time_travel % 24 != now:
        input = ''
        if time_travel % 24 < 10:
            input = '0'
        input = input + f'{time_travel % 24}'+':00'
        esteer = esteer + f'{input:6}'
        time_travel = time_travel + 3
    input = ''
    if time_travel % 24 < 10:
        input = '0'
    input = input + f'{time_travel % 24}'+':00'
    esteer = esteer + f'{input:6}'
    return esteer


def getcurrentmail(surl):
    #url = f"https://pogoda.mail.ru/prognoz/tomsk/24hours/"
    url = surl[2]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    current = soup.find("div", class_=re.compile("p-forecast__current"))
    res = re.findall('[\+,\-]\d+', current.text)
    return(int(res[0]))


def getrp5(surl):
    cookies = {
        'PHPSESSID': 'e79ea07f7364080dac2af59e7bd42f7d',
        'extreme_open': 'false',
        'ftab': '2',
        'i': '7285%7C3034%7C3646%7C5797%7C8218',
        'iru': '7285%7C3034%7C3646%7C5797%7C8218',
        'ru': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA',
        'last_visited_page': 'http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5',
        'lang': 'ru',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://yandex.ru/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Opera GX";v="119"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'PHPSESSID=e79ea07f7364080dac2af59e7bd42f7d; extreme_open=false; ftab=2; i=7285%7C3034%7C3646%7C5797%7C8218; iru=7285%7C3034%7C3646%7C5797%7C8218; ru=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5; lang=ru',
    }
    str = ''
    #url = f"https://rp5.ru/Погода_в_Томске"
    url = surl[0]
    response = requests.get(url, cookies=cookies, headers=headers)

    # rp5 weather
    soup = BeautifulSoup(response.text, "lxml")
    # title = soup.title
    # print(title.text)

    unit = soup.find("div", id="ftab_content").find(string="Температура").find_parent('tr').find_all("div", class_="t_0")
    for i in range(0, 24):
        str = str + f'{unit[i].text:6}'
    return str


def getgismeteo(surl): # 1:00 4:00 7:00 10:00 13:00 16:00 19:00 22:00
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'ax-age=0',
        'priority': 'u=0, i',
        'eferer': 'https://yandex.ru/',
        'ec-ch-ua': '"Not(A:Brand";v="99", "Opera GX";v="118", "Chromium";v="133"',
        'ec-ch-ua-mobile': '?0',
        'ec-ch-ua-platform': '"Windows"',
        'ec-fetch-dest': 'document',
        'ec-fetch-mode': 'navigate',
        'ec-fetch-site': 'cross-site',
        'ec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0'
    }

    cookies = {
        '_ym_uid': '1726717206377365778',
        '_ga': 'GA1.1.45103759.1726717208',
        '_ga_JQ0KX9JMHV': 'GS1.1.1726717208.1.1.1726717212.56.0.0',
        'ab_audience_3': '37',
        'cityUS': '4652',
        '_ym_d': '1746440110',
        '_ym_isad': '2',
        '_ym_visorc': 'b'
    }

    url = surl[1]
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    str = ''
    res = []
    unit = soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).find_all("temperature-value")
    for i in range(1, 9):
        tmp = unit[i].get('value')
        if tmp[0] == '-':
            res.append(tmp)
        else:
            tmp = '+' + tmp
            res.append(tmp)

    response = requests.get(url + 'tomorrow', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    unit = soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).find_all("temperature-value")
    for i in range(1, 9):
        tmp = unit[i].get('value')
        if tmp[0] == '-':
            res.append(tmp)
        else:
            tmp = '+' + tmp
            res.append(tmp)

    now = datetime.datetime.now().hour
    time_travel = 1
    count = 0
    while time_travel < now:
        count += 1
        time_travel = time_travel + 3

    for i in range(count, count + 8):
        str = str + f'{res[i]:6}'
    return str


def getmailru(surl):
    str = ''
    res = []
    #url = f"https://pogoda.mail.ru/prognoz/tomsk/24hours/"
    url = surl[2]
    response = requests.get(url)

    #Mail.ru weather
    soup = BeautifulSoup(response.text, "lxml")
    # title = soup.title
    # print(title.text)

    unit = soup.find_all("div", class_=re.compile("p-forecast__item"))
    for i in range(1,len(unit)):
        res = res + re.findall('[\+,\-]\d+', unit[i].text)
    for i in range(0, 24):
        str = str + f'{res[i]:6}'
    return str


def getaccuracy():
    res = [0.1, 0.1, 0.1]
    conn = psycopg2.connect(dbname='Weather_forecast', user='postgres', password='1111', host='localhost')
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute('select rp5acc(), GISMETEOacc(), MailRuacc()')
    fetch = cursor.fetchone()
    for i in range(3):
        res[i] = float(fetch[i])
    return res


def getweatherchange(param, surl):  # param: 1 = rp5, 2 = gismeteo, 3 = mailru ||| flag = 1 => =, flag = 2 => повышается, flag = 3 => понижается
    flag = -1
    curr = getcurrentmail(surl)
    if param == 1:
        cookies = {
            'PHPSESSID': 'e79ea07f7364080dac2af59e7bd42f7d',
            'extreme_open': 'false',
            'ftab': '2',
            'i': '7285%7C3034%7C3646%7C5797%7C8218',
            'iru': '7285%7C3034%7C3646%7C5797%7C8218',
            'ru': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA',
            'last_visited_page': 'http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5',
            'lang': 'ru',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://yandex.ru/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Opera GX";v="119"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'PHPSESSID=e79ea07f7364080dac2af59e7bd42f7d; extreme_open=false; ftab=2; i=7285%7C3034%7C3646%7C5797%7C8218; iru=7285%7C3034%7C3646%7C5797%7C8218; ru=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5; lang=ru',
        }
        #url = f"https://rp5.ru/Погода_в_Томске"
        url = surl[0]
        response = requests.get(url, cookies=cookies, headers=headers)
        mas = []
        # rp5 weather
        soup = BeautifulSoup(response.text, "lxml")
        # title = soup.title
        # print(title.text)

        unit = soup.find("div", id="ftab_content").find(string="Температура").find_parent('tr').find_all("div",
                                                                                                         class_="t_0")
        for i in range(0, 9):
            mas.append(int(unit[i].text))
        average = sum(mas) / len(mas)
        if abs(curr - average) < 2.0:
            flag = 1
        elif curr < average:
            flag = 2
        else:
            flag = 3
    if param == 2:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'ax-age=0',
            'priority': 'u=0, i',
            'eferer': 'https://yandex.ru/',
            'ec-ch-ua': '"Not(A:Brand";v="99", "Opera GX";v="118", "Chromium";v="133"',
            'ec-ch-ua-mobile': '?0',
            'ec-ch-ua-platform': '"Windows"',
            'ec-fetch-dest': 'document',
            'ec-fetch-mode': 'navigate',
            'ec-fetch-site': 'cross-site',
            'ec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0'
        }

        cookies = {
            '_ym_uid': '1726717206377365778',
            '_ga': 'GA1.1.45103759.1726717208',
            '_ga_JQ0KX9JMHV': 'GS1.1.1726717208.1.1.1726717212.56.0.0',
            'ab_audience_3': '37',
            'cityUS': '4652',
            '_ym_d': '1746440110',
            '_ym_isad': '2',
            '_ym_visorc': 'b'
        }

        url = surl[1]
        response = requests.get(url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        res = []
        unit = soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).find_all("temperature-value")
        for i in range(1, 9):
            tmp = unit[i].get('value')
            res.append(tmp)

        response = requests.get(url + 'tomorrow', cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        unit = soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).find_all("temperature-value")
        for i in range(1, 9):
            tmp = unit[i].get('value')
            res.append(tmp)

        now = datetime.datetime.now().hour
        time_travel = 1
        count = 0
        while time_travel < now:
            count += 1
            time_travel = time_travel + 3

        upsum = 0
        for i in range(count, count + 4):
            upsum += int(res[i])
        average = upsum / 4
        if abs(curr - average) < 2.0:
            flag = 1
        elif curr < average:
            flag = 2
        else:
            flag = 3
    if param == 3:
        res = []
        #url = f"https://pogoda.mail.ru/prognoz/tomsk/24hours/"
        url = surl[2]
        response = requests.get(url)

        # Mail.ru weather
        soup = BeautifulSoup(response.text, "lxml")
        # title = soup.title
        # print(title.text)

        unit = soup.find_all("div", class_=re.compile("p-forecast__item"))
        for i in range(1, len(unit)):
            res += re.findall('[\+,\-]\d+', unit[i].text)
        upsum = 0
        for i in range(0, 9):
            upsum += int(res[i])
        average = upsum / 9
        if abs(curr - average) < 2.0:
            flag = 1
        elif curr < average:
            flag = 2
        else:
            flag = 3
    return flag


def isThereRainfall(param, surl): #1 = rp5, 2 = GISMETEO, 3 = MailRu
    if param == 1:
        cookies = {
            'PHPSESSID': 'e79ea07f7364080dac2af59e7bd42f7d',
            'extreme_open': 'false',
            'ftab': '2',
            'i': '7285%7C3034%7C3646%7C5797%7C8218',
            'iru': '7285%7C3034%7C3646%7C5797%7C8218',
            'ru': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA',
            'last_visited_page': 'http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5',
            'lang': 'ru',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://yandex.ru/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Opera GX";v="119"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'PHPSESSID=e79ea07f7364080dac2af59e7bd42f7d; extreme_open=false; ftab=2; i=7285%7C3034%7C3646%7C5797%7C8218; iru=7285%7C3034%7C3646%7C5797%7C8218; ru=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%7C%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3%7C%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C%7C%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%7C%D0%A2%D0%BE%D0%BC%D1%81%D0%BA; last_visited_page=http%3A%2F%2Frp5.ru%2F%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D0%BE%D0%BC%D1%81%D0%BA%D0%B5; lang=ru',
        }

        now = datetime.datetime.now()
        str = ''
        url = surl[0]
        response = requests.get(url, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")
        unit = (soup.find("table", id="forecastTable_1_3").find(string="Осадки, мм").
                find_parent('tr').find_all("div",class_="pr_0"))
        for i in range(0, 23 - now.hour):
            str = str + unit[i].get('onmouseover')
        if 'дождь' in str or 'снег' in str or 'град' in str:
            return 1
        else:
            return 0
    elif param == 2:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'ax-age=0',
            'priority': 'u=0, i',
            'eferer': 'https://yandex.ru/',
            'ec-ch-ua': '"Not(A:Brand";v="99", "Opera GX";v="118", "Chromium";v="133"',
            'ec-ch-ua-mobile': '?0',
            'ec-ch-ua-platform': '"Windows"',
            'ec-fetch-dest': 'document',
            'ec-fetch-mode': 'navigate',
            'ec-fetch-site': 'cross-site',
            'ec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0'
        }

        cookies = {
            '_ym_uid': '1726717206377365778',
            '_ga': 'GA1.1.45103759.1726717208',
            '_ga_JQ0KX9JMHV': 'GS1.1.1726717208.1.1.1726717212.56.0.0',
            'ab_audience_3': '37',
            'cityUS': '4652',
            '_ym_d': '1746440110',
            '_ym_isad': '2',
            '_ym_visorc': 'b'
        }

        url = surl[1]
        response = requests.get(url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        unit = soup.find("div", class_=re.compile("widget-row-icon")).find_all("div", class_="row-item")
        flag = 0
        for i in range(3, len(unit)):
            sus = unit[i].get('data-tooltip')
            if 'дождь' in sus or 'снег' in sus or 'град' in sus:
                flag = 1
        return flag
    elif param == 3:
        now = datetime.datetime.now()
        str = ''
        url = surl[2]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        unit = soup.find("div", class_=re.compile("p-forecast__grid")).find_all("span", class_=re.compile(
            "p-forecast__subtext"))
        i = 0
        while i < 23 - now.hour:
            str = str + unit[i * 2].text + '|'
            i = i + 1
        if 'дождь' in str or 'снег' in str or 'град' in str:
            return 1
        else:
            return 0
    return -1


def gismNotify(surl):
    flag = isThereRainfall(2, surl)
    if flag == 0:
        return 'Самый точный (на данный момент) сайт GISMETEO считает, что сегодня не будет никаких осадков. Если что, вы знаете, кого винить.'
    elif flag == 1:
        return 'Самый точный (на данный момент) сайт GISMETEO считает, что сегодня вам стоило бы взять зонтик (даже он иногда может говорить правду, советую прислушаться).'
    else:
        return  'Ошибка в проверке на осадки. Свяжитесь с автором приложения с просьбой исправить проблему'


def rp5Notify(surl):
    flag = isThereRainfall(1, surl)
    if flag == 1:
        return 'Сайт rp5 (мой любимчик) считает, что сегодня вам стоило бы взять зонтик (лучше с ним и без дождя, чем без него и под дождём).'
    elif flag == 0:
        return 'Сайт rp5 (мой любимчик) считает, что сегодня не будет никаких осадков. Если всё же осадки были, то это явно не его вина.'
    else:
        return 'Ошибка в проверке на осадки. Свяжитесь с автором приложения с просьбой исправить проблему'


def MailRuNotify(surl):
    flag = isThereRainfall(3, surl)
    if flag == 1:
        return 'Сайт - почтальон MailRu считает, что сегодня вам необходим напарник - зонтик. Пока дождь не доставляется почтой россии, всё должно быть в порядке.'
    elif flag == 0:
        return 'Сайт - почтальон MailRu считает, что сегодня не будет никаких осадков. Жалобы в ответ на это письмо отправлять не стоит, я не несу за это ответственности.'
    else:
        return 'Ошибка в проверке на осадки. Свяжитесь с автором приложения с просьбой исправить проблему'


def gismRainfall(surl):
    flag = isThereRainfall(2, surl)
    if flag == 0:
        return 'Осадки не ожидаются'
    elif flag == 1:
        return 'Ожидаются осадки'
    else:
        return 'Невозможно спрогнозировать осадки'


def rp5Rainfall(surl):
    flag = isThereRainfall(1, surl)
    if flag == 0:
        return 'Осадки не ожидаются'
    elif flag == 1:
        return 'Ожидаются осадки'
    else:
        return 'Невозможно спрогнозировать осадки'


def mailRainfall(surl):
    flag = isThereRainfall(3, surl)
    if flag == 0:
        return 'Осадки не ожидаются'
    elif flag == 1:
        return 'Ожидаются осадки'
    else:
        return 'Невозможно спрогнозировать осадки'


def send_simple_email(receiver_email = '', surl = ['','','']):
    sender_email = "weather_guard@mail.ru"
    subject = "Прогноз погоды"
    smtp_server = "smtp.mail.ru"
    smtp_port = 587
    login = "weather_guard@mail.ru"
    password = "UaZiyr9txYeUcRBJgjae"
    res = [0.1, 0.1, 0.1]
    conn = psycopg2.connect(dbname='Weather_forecast', user='postgres',
                            password='1111', host='localhost')
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute('select rp5acc(), GISMETEOacc(), MailRuacc()')
    fetch = cursor.fetchone()
    for i in range(3):
        res[i] = float(fetch[i])
    maxim = max(res)
    if maxim == res[0]: #rp5
        body = rp5Notify(surl)
    elif maxim == res[1]: #GISMETEO
        body = gismNotify(surl)
    else:
        body = MailRuNotify(surl)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)
    try:
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Письмо отправлено')
        server.quit()
        return schedule.CancelJob
    except:
        print('Письмо не отправлено (адресс введён некорректно)')
        return schedule.CancelJob


def save_queue_to_json(queue, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(list(queue), f, ensure_ascii=False, indent=4)

def load_queue_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return list(list(item) for item in data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        res = getaccuracy()
        self.mailbox = ''
        self.sendtime = '08:00'
        self.url = {
            'Москва' : [f'https://rp5.ru/Погода_в_Москве_(ВДНХ)', f'https://www.gismeteo.ru/weather-moscow-4368/',f'https://pogoda.mail.ru/prognoz/moskva/24hours/'],
            'Томск' : [f'https://rp5.ru/Погода_в_Томске',f'https://www.gismeteo.ru/weather-tomsk-4652/',f'https://pogoda.mail.ru/prognoz/tomsk/24hours/'],
            'Новосибирск' : [f'https://rp5.ru/Погода_в_Новосибирске', f'https://www.gismeteo.ru/weather-novosibirsk-4690/', f'https://pogoda.mail.ru/prognoz/novosibirsk/24hours/'],
            'Санкт-Петербург' : [f'https://rp5.ru/Погода_в_Санкт-Петербурге', f'https://www.gismeteo.ru/weather-sankt-peterburg-4079/', f'https://pogoda.mail.ru/prognoz/sankt_peterburg/24hours/'],
            'Екатеринбург' : [f'https://rp5.ru/Погода_в_Екатеринбурге', f'https://www.gismeteo.ru/weather-yekaterinburg-4517/', f'https://pogoda.mail.ru/prognoz/ekaterinburg/24hours/'],
            'Казань' : [f'https://rp5.ru/Погода_в_Казани,_Татарстан', f'https://www.gismeteo.ru/weather-kazan-4364/', f'https://pogoda.mail.ru/prognoz/kazan/24hours/'],
            'Нижний Новгород' : [f'https://rp5.ru/Погода_в_Нижнем_Новгороде', f'https://www.gismeteo.ru/weather-nizhny-novgorod-4355/', f'https://pogoda.mail.ru/prognoz/nizhniy_novgorod/24hours/']
        }

        self.setWindowTitle("Weather Forecast")
        self.setFixedSize(800,600)
        self.setObjectName('win')  # Set the window name, which is equivalent to the ID in CSS
        self.setStyleSheet('#win{border-image:url(mainmenu.png);}')
        labelfont = QFont("Monospace", 15)

        self.citybox = QComboBox()
        self.citybox.setFont(labelfont)
        self.citybox.addItems(['Москва', 'Томск', 'Новосибирск', 'Санкт-Петербург', 'Екатеринбург', 'Казань', 'Нижний Новгород'])
        self.citybox.setCurrentIndex(1)
        self.citybox.currentTextChanged.connect(self.citybox_changed)

        self.button1 = QPushButton("Показать погоду")
        self.button1.setFont(labelfont)
        self.button1.clicked.connect(self.the_button1_was_clicked)
        self.button2 = QPushButton("Показать погоду")
        self.button2.setFont(labelfont)
        self.button2.clicked.connect(self.the_button2_was_clicked)
        self.button3 = QPushButton("Показать погоду")
        self.button3.setFont(labelfont)
        self.button3.clicked.connect(self.the_button3_was_clicked)

        testLabel1 = QLabel("Сайт rp5")
        testLabel2 = QLabel("Сайт GISMETEO")
        testLabel3 = QLabel("Сайт Mail.ru")
        testLabel1.setFont(labelfont)
        testLabel2.setFont(labelfont)
        testLabel3.setFont(labelfont)
        testLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        testLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        testLabel3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.testLabel4 = QLabel('Погода *название сайта*:')
        self.testLabel4.setFont(labelfont)
        self.testLabel4.setVisible(False)
        self.testLabel4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.testLabel5 = QLabel('Осадки:')
        self.testLabel5.setFont(labelfont)
        self.testLabel5.setVisible(False)
        self.testLabel5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label1 = QLabel("Точность:")
        label1.setFont(labelfont)
        label2 = QLabel("Точность:")
        label2.setFont(labelfont)
        label3 = QLabel("Точность:")
        label3.setFont(labelfont)

        self.cold = QPixmap("arrowCold.png")
        self.hot = QPixmap("arrowHot.png")
        self.mid = QPixmap("arrowMid.png")

        rp5w = getweatherchange(1, self.url[self.citybox.currentText()])
        gismw = getweatherchange(2, self.url[self.citybox.currentText()])
        mailw = getweatherchange(3, self.url[self.citybox.currentText()])

        self.tlabel1 = QLabel()
        if rp5w == 1:
            self.tlabel1.setPixmap(self.mid)
        elif rp5w == 2:
            self.tlabel1.setPixmap(self.hot)
        elif rp5w == 3:
            self.tlabel1.setPixmap(self.cold)
        self.tlabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tlabel2 = QLabel()
        if gismw == 1:
            self.tlabel2.setPixmap(self.mid)
        elif gismw == 2:
            self.tlabel2.setPixmap(self.hot)
        elif gismw == 3:
            self.tlabel2.setPixmap(self.cold)
        self.tlabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tlabel3 = QLabel()
        if mailw == 1:
            self.tlabel3.setPixmap(self.mid)
        elif mailw == 2:
            self.tlabel3.setPixmap(self.hot)
        elif mailw == 3:
            self.tlabel3.setPixmap(self.cold)
        self.tlabel3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line1 = QLineEdit(str(res[0]))
        self.line1.setReadOnly(True)
        self.line1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line1.setMaximumSize(50, 10000)
        self.line1.setFont(labelfont)
        self.line2 = QLineEdit(str(res[1]))
        self.line2.setReadOnly(True)
        self.line2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line2.setMaximumSize(50, 10000)
        self.line2.setFont(labelfont)
        self.line3 = QLineEdit(str(res[2]))
        self.line3.setReadOnly(True)
        self.line3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line3.setMaximumSize(50, 10000)
        self.line3.setFont(labelfont)
        # self.line4 = QLineEdit('*Предсказание погоды с текущего часа и до конца дня*')
        # self.line4.setReadOnly(True)
        # self.line4.setVisible(False)

        font = QFont("Monospace", 15)
        font.setFixedPitch(True)
        # font.setFamily("Monospace")
        self.widg1 = QListWidgetItem()
        self.widg1.setFont(font)
        self.widg1.setText('Время Время Время Время Время Время Время Время Время Время Время')
        self.widg2 = QListWidgetItem()
        self.widg2.setFont(font)
        self.widg2.setText('Погода Погода Погода Погода Погода Погода Погода Погода Погода Погода Погода')
        self.listwidget = QListWidget()
        self.listwidget.addItem(self.widg1)
        self.listwidget.addItem(self.widg2)
        self.listwidget.setMaximumHeight(80)
        self.listwidget.setVisible(False)


        notifylabel = QLabel("Уведомления об осадках присылать на почту:")
        notifylabel.setFont(labelfont)
        self.notifyline = QLineEdit()
        self.notifyline.setMaximumSize(300, 1000)
        self.notifyline.setFont(labelfont)
        self.notifybox = QComboBox()
        self.notifybox.setFont(labelfont)
        self.notifybox.addItems(['05:00','06:00','07:00','08:00','09:00','10:00'])
        self.notifybox.setCurrentIndex(3)
        self.notifybox.setMinimumWidth(140)
        self.notifybutton = QPushButton('Сохранить')
        self.notifybutton.setFont(labelfont)
        self.notifybutton.setMinimumWidth(140)
        self.notifybutton.clicked.connect(self.the_notifybutton_was_clicked)


        # Устанавливаем центральный виджет Window.
        layout1_1 = QVBoxLayout()
        layout1_1.addWidget(label1)
        layout1_1.addWidget(self.line1)

        layout1_2 = QVBoxLayout()
        layout1_2.addWidget(label2)
        layout1_2.addWidget(self.line2)

        layout1_3 = QVBoxLayout()
        layout1_3.addWidget(label3)
        layout1_3.addWidget(self.line3)

        NotifyLayout = QHBoxLayout()
        NotifyLayout.addStretch()
        NotifyLayout.addWidget(notifylabel)
        NotifyLayout.addWidget(self.notifyline)
        NotifyLayout.addWidget(self.notifybox)
        NotifyLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        NotifyButLayout = QHBoxLayout()
        NotifyButLayout.addStretch()
        NotifyButLayout.addWidget(self.notifybutton)
        NotifyButLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        cityLayout = QVBoxLayout()
        cityLayout.addWidget(self.citybox)
        cityLayout.addStretch()
        cityLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QVBoxLayout()
        layout1.addStretch()
        layout1.addWidget(testLabel1)
        layout1.addStretch()
        layout1.addWidget(testLabel2)
        layout1.addStretch()
        layout1.addWidget(testLabel3)
        layout1.addStretch()

        layout2 = QVBoxLayout()
        layout2.addStretch()
        layout2.addWidget(self.button1)
        layout2.addStretch()
        layout2.addWidget(self.button2)
        layout2.addStretch()
        layout2.addWidget(self.button3)
        layout2.addStretch()

        layout3 = QVBoxLayout()
        layout3.addStretch()
        layout3.addLayout(layout1_1)
        layout3.addStretch()
        layout3.addLayout(layout1_2)
        layout3.addStretch()
        layout3.addLayout(layout1_3)
        layout3.addStretch()

        layout4 = QVBoxLayout()
        layout4.addStretch()
        layout4.addWidget(self.tlabel1)
        layout4.addStretch()
        layout4.addWidget(self.tlabel2)
        layout4.addStretch()
        layout4.addWidget(self.tlabel3)
        layout4.addStretch()

        wraplayout = QHBoxLayout()
        wraplayout.addStretch()
        wraplayout.addLayout(layout1)
        wraplayout.addStretch()
        wraplayout.addLayout(layout2)
        wraplayout.addStretch()
        wraplayout.addLayout(layout3)
        wraplayout.addLayout(layout4)
        wraplayout.addStretch()

        layout5 = QVBoxLayout()
        layout5.addLayout(cityLayout)
        layout5.addStretch()
        layout5.addLayout(wraplayout)
        layout5.addWidget(self.testLabel4)
        layout5.addWidget(self.listwidget)
        layout5.addWidget(self.testLabel5)
        layout5.addStretch()
        layout5.addLayout(NotifyLayout)
        layout5.addLayout(NotifyButLayout)
        #layout5.addStretch()

        container = QWidget()
        container.setLayout(layout5)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

        #schedule.every().day.at('08:00').do(send_simple_email, receiver_email=self.notifyline.text())


    def the_button1_was_clicked(self):
        #print("Clicked!")
        self.setStyleSheet('#win{border-image:url(rp5.png);}')
        self.button1.setEnabled(False)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)
        self.testLabel4.setText('Погода rp5:')
        self.testLabel5.setText(rp5Rainfall(self.url[self.citybox.currentText()]))
        self.widg1.setText(get1htime())
        self.widg2.setText(getrp5(self.url[self.citybox.currentText()]))
        self.listwidget.setVisible(True)
        self.testLabel4.setVisible(True)
        self.testLabel5.setVisible(True)
        self.listwidget.setFocus()


    def the_button2_was_clicked(self):
        #print("Clicked!")
        self.setStyleSheet('#win{border-image:url(GISMETEO.png);}')
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        self.button3.setEnabled(True)
        self.testLabel4.setText('Погода GISMETEO:')
        self.testLabel5.setText(gismRainfall(self.url[self.citybox.currentText()]))
        self.widg1.setText(get3htime())
        self.widg2.setText(getgismeteo(self.url[self.citybox.currentText()]))
        self.listwidget.setVisible(True)
        self.testLabel4.setVisible(True)
        self.testLabel5.setVisible(True)
        self.listwidget.setFocus()

    def the_button3_was_clicked(self):
        #print("Clicked!")
        self.setStyleSheet('#win{border-image:url(MailRu.png);}')
        self.button3.setEnabled(False)
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.testLabel4.setText('Погода MailRu:')
        self.testLabel5.setText(mailRainfall(self.url[self.citybox.currentText()]))
        self.widg1.setText(get1htime())
        self.widg2.setText(getmailru(self.url[self.citybox.currentText()]))
        self.listwidget.setVisible(True)
        self.testLabel4.setVisible(True)
        self.testLabel5.setVisible(True)
        self.listwidget.setFocus()


    def the_notifybutton_was_clicked(self):
        self.mailbox = self.notifyline.text()
        self.sendtime = self.notifybox.currentText()
        save_queue_to_json([[self.sendtime], [self.mailbox]],'notify')
        schedule.every().day.at(self.sendtime).do(send_simple_email, receiver_email=self.mailbox, surl=self.url[self.citybox.currentText()])


    def citybox_changed(self):
        self.setStyleSheet('#win{border-image:url(mainmenu.png);}')
        self.button2.setEnabled(True)
        self.button1.setEnabled(True)
        self.button3.setEnabled(True)
        self.listwidget.setVisible(False)
        self.testLabel4.setVisible(False)
        self.testLabel5.setVisible(False)
        rp5w = getweatherchange(1, self.url[self.citybox.currentText()])
        gismw = getweatherchange(2, self.url[self.citybox.currentText()])
        mailw = getweatherchange(3, self.url[self.citybox.currentText()])
        if rp5w == 1:
            self.tlabel1.setPixmap(self.mid)
        elif rp5w == 2:
            self.tlabel1.setPixmap(self.hot)
        elif rp5w == 3:
            self.tlabel1.setPixmap(self.cold)

        if gismw == 1:
            self.tlabel2.setPixmap(self.mid)
        elif gismw == 2:
            self.tlabel2.setPixmap(self.hot)
        elif gismw == 3:
            self.tlabel2.setPixmap(self.cold)

        if mailw == 1:
            self.tlabel3.setPixmap(self.mid)
        elif mailw == 2:
            self.tlabel3.setPixmap(self.hot)
        elif mailw == 3:
            self.tlabel3.setPixmap(self.cold)


async def Notify():
    while True:
        schedule.run_pending()
        await asyncio.sleep(10)

async def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()

    loop.create_task(Notify())
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
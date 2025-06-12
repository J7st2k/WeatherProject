import time

import requests
import re
import os
import psycopg2
from bs4 import BeautifulSoup
import datetime
import schedule
import json


def getrp5stat():
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
    url = f"https://rp5.ru/Погода_в_Томске"
    response = requests.get(url, cookies=cookies, headers=headers)
    mas = []
    soup = BeautifulSoup(response.text, "lxml")

    unit = (soup.find("div", id="ftab_content").find(string="Температура").find_parent('tr').
            find_all("div", class_="t_0"))
    for i in range(0, 24):
        mas.append(unit[i].text)
    return mas[17]


def getgismeteostat():  # 1:00 4:00 7:00 10:00 13:00 16:00 19:00 22:00
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

    response = requests.get('https://www.gismeteo.ru/weather-tomsk-4652/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    res = []
    unit = (soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).
            find_all("temperature-value"))
    for i in range(1, 9):
        tmp = unit[i].get('value')
        if tmp[0] == '-':
            res.append(tmp)
        else:
            tmp = '+' + tmp
            res.append(tmp)

    response = requests.get('https://www.gismeteo.ru/weather-tomsk-4652/tomorrow', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    unit = (soup.find("div", class_=re.compile("widget-row-chart-temperature-air")).
            find_all("temperature-value"))
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

    return res[count + 6]

def getmailrustat():
    res = []
    url = f"https://pogoda.mail.ru/prognoz/tomsk/24hours/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    unit = soup.find_all("div", class_=re.compile("p-forecast__item"))
    for i in range(1,len(unit)):
        res = res + re.findall('[\+,\-]\d+', unit[i].text)
    return res[17]

def getcurrent():
    currtemp = [0,0,0]
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

    url = f"https://rp5.ru/Погода_в_Томске"
    response = requests.get(url, cookies=cookies, headers=headers)

    # rp5 weather
    soup = BeautifulSoup(response.text, "lxml")
    unit = soup.find("div", id="ArchTemp").find_all("span", class_="t_0")
    tmp = re.findall(f"\d+", unit[0].text)
    currtemp[0] = int(tmp[0])

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

    response = requests.get('https://www.gismeteo.ru/weather-tomsk-4652/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    unit = soup.find("div", class_=re.compile("weather")).find_all("temperature-value")
    currtemp[1] = int(unit[0].get('value'))

    url = f"https://pogoda.mail.ru/prognoz/tomsk/24hours/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    current = soup.find("div", class_=re.compile("p-forecast__current"))
    res = []
    res = re.findall('[\+,\-]\d+', current.text)
    currtemp[2] = int(res[0])

    return currtemp

def insertdata():
    conn = psycopg2.connect(dbname='Weather_forecast', user='postgres', password='1111', host='localhost')
    cursor = conn.cursor()
    conn.autocommit = True
    que = load_queue_from_json('test')
    result = que[0]
    curr = getcurrent()
    cursor.execute('insert into predicts (rp5, GISMETEO, MailRu, rp5curr, gismeteocurr, mailrucurr) values (%s,%s,%s,%s,%s,%s);',
                   (result[0], result[1], result[2], curr[0], curr[1], curr[2]))
    que.pop(0)
    que.append([getrp5stat(), getgismeteostat(), getmailrustat()])
    save_queue_to_json(que, 'test')


def save_queue_to_json(queue, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(list(queue), f, ensure_ascii=False, indent=4)

def load_queue_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return list(list(item) for item in data)


def schedule_first_run():
    now = datetime.datetime.now()

    target_time = datetime.datetime(now.year, now.month, now.day, 1, 0)
    if now >= target_time:
        target_time += datetime.timedelta(days=1)

    delta = target_time - now
    seconds_until_target = delta.total_seconds()

    schedule.every(seconds_until_target).seconds.do(first_run_job)


def first_run_job():
    insertdata()
    schedule.every(3).hours.do(insertdata)
    return schedule.CancelJob


def main():
    schedule_first_run()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()

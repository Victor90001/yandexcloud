import csv
import os
import json
import sys
import time
import pandas
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options


class Token:
    def __init__(self):
        with open('csv/auth.csv', newline='') as csvfile:
            read = csv.reader(csvfile, delimiter=',', quotechar='|')
            heads = next(read)
            first_row = next(read)
            self.bearer = first_row[1]
        self.client_id = ''
        self.__auth_code = ''

    def generate_bearer(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.__auth_code,
            'grant_type': 'client_credentials',
        }
        try:
            response = requests.post('https://id.twitch.tv/oauth2/token', headers=header, data=data).json()
            self.bearer = response['access_token']
            df = pandas.DataFrame.from_dict([response])
            df.to_csv('csv/auth.csv')
        except Exception as e:
            print(e)


class Requests:
    __BEARER = "Bearer "

    def __init__(self):
        # self.__BEARER = "Bearer "
        self.myToken = Token()
        self.headers = {
            'Client-ID': self.myToken.client_id,
            'Authorization': self.__BEARER + self.myToken.bearer
        }

    def generate_new_bearer(self):
        self.myToken.generate_bearer()
        self.headers['Authorization'] = self.__BEARER + self.myToken.bearer


req = Requests()


def get_followers(chanel):
    url = f"https://twitchtracker.com/{chanel}/statistics"
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument(f'user-agent={useragent}')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    elements = driver.find_elements(By.ID, 'DataTables_Table_1_wrapper')[0]
    header = ['Month', 'Gain Followers', 'Followers', 'Gain Views', 'Total Views']
    data = []
    for tr in elements.find_elements(By.TAG_NAME, 'tr'):
        row = {}
        for i,td in enumerate(tr.find_elements(By.TAG_NAME, 'td')):
            row[header[i]] = td.text
        if len(row) > 0:
            data.append(row)
    driver.quit()
    return {'data': data}


if len(sys.argv)==2:
    fls = get_followers(sys.argv[1])
    print(fls)
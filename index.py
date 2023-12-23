import csv
import os
import json
import time
import pandas
import requests

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
            raise Exception("Sorry, something wrong")

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

def search_users(search_name, after_key=''):
    if len(after_key) == 0:
        params = {'query': search_name}
        response = requests.get('https://api.twitch.tv/helix/search/channels',
                                headers=req.headers,
                                params=params).json()
        print(json.dumps(response, indent=2, ensure_ascii=False))
        return response
    else:
        params = {'query': search_name, 'after': after_key}
        response = requests.get('https://api.twitch.tv/helix/search/channels',
                                headers=req.headers,
                                params=params).json()
        print(json.dumps(response, indent=2, ensure_ascii=False))
        return response

def get_users(user_id):
    params = {'id': user_id}
    response = requests.get('https://api.twitch.tv/helix/users',
                            headers=req.headers,
                            params=params).json()
    return response

def channel_info(channel_id):
    params = {'broadcaster_id': channel_id}
    response = requests.get('https://api.twitch.tv/helix/channels',
                            headers=req.headers,
                            params=params).json()
    return response

def get_stream_live_info(channel_ids=None, channel_names=None, game_ids=None, language=None, rtype='live'):
    params = []
    if channel_ids is not None:
        for ch_id in channel_ids:
            params.append(('user_id', ch_id))
    if channel_names is not None:
        for ch_name in channel_names:
            params.append(('user_login', ch_name))
    if game_ids is not None:
        for game in game_ids:
            params.append(('game_id', game))
    params.append(('language', language))
    params.append(('type', rtype))
    response = requests.get('https://api.twitch.tv/helix/streams', headers=req.headers, params=params).json()
    print(json.dumps(response, indent=2, ensure_ascii=False))

def channel_followers(channel_id):
    params = {'broadcaster_id': channel_id}
    response = requests.get('https://api.twitch.tv/helix/channels/followers', headers=req.headers, params=params).json()
    return response

def handler(event, context):
    data = {}
    if 'search' in event:
        data['channels']=search_users(event['search'])
    if 'channel_info' in event:
        data['info'] = channel_info(event['channel_info'])
    if 'cur_followers' in event:
        data['cur_followers'] = channel_followers(event['cur_followers'])
    if 'user' in event:
        data['user'] = get_users(event['user'])
    return {
        'statusCode': 200,
        'data': data
    }

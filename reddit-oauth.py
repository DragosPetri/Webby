import requests
import pandas as pd
from datetime import datetime

def df_from_response(res):
    df = pd.DataFrame(columns=['flair','title','selftext','ups','downs','id','kind'])

    for post in res.json()['data']['children']:
        if post['data']['link_flair_css_class']!='meme':
            if post['data']['link_flair_css_class']!='shitpost' :
                df = df.append({
                    'title': post['data']['title'],
                    'selftext': post['data']['selftext'],
                    'ups': post['data']['ups'],
                    'downs': post['data']['downs'],
                    'flair': post['data']['link_flair_css_class'],
                    'id': post['data']['id'],
                    'kind': post['kind']
                }, ignore_index=True)

    return df

auth = requests.auth.HTTPBasicAuth('############', '####################')

data = {'grant_type': 'password',
        'username': '########',
        'password': '########'}

headers = {'User-Agent': '############'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
token = f"bearer {res.json()['access_token']}"
headers = {**headers, **{'Authorization': token}}

data = pd.DataFrame()
params = {'limit': 50}



for i in range(1):
    res = requests.get('https://oauth.reddit.com/r/wallstreetbets/hot/',
                       headers=headers,
                       params=params)

    new_df = df_from_response(res)
    row = new_df.iloc[len(new_df)-1]
    fullname = row['kind'] + '_' + row['id']
    params['after'] = fullname
    
    data = data.append(new_df, ignore_index=True)

data.to_csv("table.csv")    
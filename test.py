import requests

email = 'sct_mahou@sctech.es'
password = '000000'
data = {
    'email': email,
    'password': password
}
response = requests.post('https://push.bigtincan.com/v5/webapi/signin', data=data)
data = response.json()
print(data)
token = data['oauth2']['access_token']
print('access token - {}'.format(token))
headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Origin': 'https://appnext.bigtincan.com',
            'Referer': 'Sec-Fetch-Mode',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
tabs = requests.get(
        'https://push.bigtincan.com/v5/webapi/content/tabs',
        params={
            'limit': 100,
            'offset': 0,
            'sort_by': 'name',
            'show_hidden_channels': 0
        },
        headers=headers
    )
tabs = tabs.json()
print (tabs)
tabs_ordered = []
channels_tab = []
stories_channel = []

for tab in tabs:
    print ('* tab *')
    tab_name = tab['name']
    tab_id = tab['id']
    channels_request = requests.get(
        'https://push.bigtincan.com/v5/webapi/content/channels?tab_id={}'.format(tab_id),
        headers=headers
    )
    print ('- {}'.format(tab_name))
    print(' -- channels de '.format(tab_name))
    channels = channels_request.json()
    for channel in channels:
        print(' -- ** channel **')
        channel_name = channel['name']
        print(' ---- {}'.format(channel_name))
        print (' ----- *** stories - {} ***'.format(channel_name))
        channel_id = channel['id']
        stories_request = requests.get(
            'https://push.bigtincan.com/v5/webapi/content/stories?channel_id={}'.format(channel_id),
            headers=headers
        )
        stories = stories_request.json()
        for story in stories:
            name = story['name']
            print(' ------- {} '.format(name))
            stories_channel.append(story['name'])
        print (' ----- *** stories - {} ***'.format(channel_name))
        channels_tab.append({channel_name: stories_channel})
        stories_channel = []
    tabs_ordered.append({tab_name: channels_tab})
    channels_tab = []

print (tabs_ordered)
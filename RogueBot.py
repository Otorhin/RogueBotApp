import requests

API = 'https://rogue.iliago.tk/api/'
ddd = ''

def get_message(token):
    url = API + str(token) + '/messages?clear=True'
    get_url = requests.get(url)
    text = ''
    button = []
    if get_url.status_code == 200 :
        if not get_url.json():
            send_message(token, 'Start')
            get_url = requests.get(url)
        for all in get_url.json():
            if all['buttons']:
                for alls in all['buttons']:
                    if type(alls) == type(ddd):
                        if alls not in button:
                            button.append(alls)
                    else:
                        for allls in alls:
                            if allls not in button:
                                button.append(allls)
            if all['text']:
                if all['text'] not in text:
                    text += '\n' + all['text']
        return(text, button)
    else:
        text = 'Вы не авторизированы.'
        button = []
        return (text, button)

def send_message(token, message):
    print(token)
    print(message)
    url = API + str(token) + '/send?message=' + str(message)
    get_url = requests.get(url)
    if get_url.status_code == 200:
        return True
    else :
        return False

def validate(token):
    url = API + str(token) + '/validate'
    get_url = requests.get(url)
    if get_url.status_code == 200:
        return True
    else :
        return False


def Test(lel):
    print(lel)
    type(lel)
from bs4 import BeautifulSoup as Bs
from requests import get
from playsound import playsound
from os.path import join, exists

header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/531.4 (KHTML, like Gecko) '
                        'Chrome/3.0.194.0 Safari/531.4'}


def path_en(word):
    return join('assets', 'sounds', f'{word}_en.mp3')


def path_us(word):
    return join('assets', 'sounds', f'{word}_us.mp3')


def play(path):
    playsound(path)


def soup_result(word):
    try:
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
        response = get(url, headers=header)
        if response.status_code == 200:
            soup = Bs(response.text, "html.parser")
            return soup
    except:
        pass


def find_elements(soup, word, acs=None):
    try:
        voice_url = None
        divs = soup.findAll('div', {'class': 'sound'})
        for div in divs:
            if acs in div['title']:
                if f'{word}' not in div['data-src-mp3']:
                    continue
                voice_url = div['data-src-mp3']
                break
        return voice_url
    except:
        pass


def req(word, url, x):
    response = get(url, headers=header)
    try:
        if x == 'EN':
            with open(f'{path_en(word)}', 'wb') as f:
                f.write(response.content)
        else:
            with open(f'{path_us(word)}', 'wb') as f:
                f.write(response.content)
        return True
    except:
        return None


def down(x, word, p):
    res = soup_result(word)
    if res:
        if x == 'EN':
            url = find_elements(res, word, 'English')
        else:
            url = find_elements(res, word, 'American')

        if url:
            req_res = req(word, url, x)
            if req_res:
                play(p)
                return True
    else:
        return False


def play_sound(word, x):
    if x == 'EN':
        file_path = path_en(word)
    else:
        file_path = path_us(word)

    if not exists(file_path):
        return False
    else:
        play(file_path)
        return True


def down_sound(word, x):
    if x == 'EN':
        file_path = path_en(word)
    else:
        file_path = path_us(word)
    return down(x, word, file_path)


def to_pronun(word, x):
    try:
        if x == 'EN':
            file_path = path_en(word)
        else:
            file_path = path_us(word)
        if exists(file_path):
            play(file_path)
        else:
            down(x, word, file_path)
    except:
        return False

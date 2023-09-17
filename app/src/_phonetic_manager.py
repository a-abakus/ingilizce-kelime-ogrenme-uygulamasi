from app.src._database_manager import add_phon
from bs4 import BeautifulSoup as Bs
from requests import get


count = 0
header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/531.4 (KHTML, like Gecko) '
                        'Chrome/3.0.194.0 Safari/531.4'}


def soup_result(word):
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    response = get(url, headers=header)
    if response.status_code == 200:
        soup = Bs(response.text, "html.parser")
        return soup


def get_and_add_phn(soup, word, x):
    try:
        phon = soup.findAll('span', {'class': 'phon'})
        phons = []
        for x in phon:
            if len(phons) > 1:
                break
            phons.append(x.getText().replace("/", "").replace("ː", ":"))
        if x == "add":
            if phons:
                add_phon(word, phons)
                return phons
        else:
            return phons
    except:
        pass


def phon_to_pronun(word, x):
    phonetic = get_and_add_phn(soup_result(word), word, x)
    if phonetic is None or len(phonetic) == 0:
        return None
    else:
        return phonetic


def phon_to_word(word):
    global count
    count = 0
    get_phonetic = get_and_add_phn(soup_result(word), word, "add")
    if get_phonetic is None or len(get_phonetic) == 0:
        count += 1
        error = "wrong"
        if count > 1:
            count = 0
            return None
        else:
            return error
    count = 0
    return get_phonetic

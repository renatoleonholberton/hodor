import requests
import pytesseract
from bs4 import BeautifulSoup

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Renato\AppData\Local\Programs\Tesseract-OCR\tesseract'

def get_payload(res):
    """Generates the payload needed to be send"""
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.form
    key_input = form.find('input', {'name': 'key'})
    
    captcha_text = pytesseract.image_to_string(r'captcha.png')

    return {
        'id': '2829',
        'captcha': captcha_text[:4],
        'holdthedoor': 'Submit',
        'key': key_input['value']
    }

def request_captcha(session):
    """Makes a get request to get the captcha"""
    res = session.get('http://158.69.76.135/captcha.php')
    with open('captcha.png', mode='wb') as file:
        file.write(res.content)


def get_headers(url):
    """Creates a dictionary for requests headers"""
    # needed to bypass referer and webscrape detector
    return {
        'referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }


def send_request(url, session):
    """Sends the requests to make one vote"""
    res = session.get(url)
    request_captcha(session)
    payload = get_payload(res)
    headers = get_headers(url)
    session.headers.update(headers)
    res = session.post(url, data=payload)

    return len(res.text) > 100


def make_sync_request(url, total_req=1):
    """Make sequential requests to an endpoint"""
    success, sended_req = 0, 0
    with requests.session() as session:
        while success < total_req:
            if send_request(url, session):
                success += 1
            sended_req += 1

    print('Success rate: {}% ({}/{})'.format(success * 100/ sended_req, success, sended_req))


# 0: invalid id
# 5: Wrong key value
# 6: not keywas sended
# 7: Wrong referer
# 9: No scripts allowed, you need to be human
# 11: bad captcha
import requests
import pytesseract
from bs4 import BeautifulSoup
blur = __import__('process_img').blur


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Renato\AppData\Local\Programs\Tesseract-OCR\tesseract'

def get_payload(res):
    """Generates the payload needed to be send"""
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.form
    key_input = form.find('input', {'name': 'key'})

    img = blur('captcha.png')
    captcha_text = pytesseract.image_to_string(img)

    return {
        'id': '2829',
        'captcha': captcha_text[:8],
        'holdthedoor': 'Submit',
        'key': key_input['value']
    }


def get_captcha(session):
    """Reuests a captcha and stores the image as 'captcha.png'"""
    # get captcha
    res = session.get('http://158.69.76.135/tim.php')
    with open('captcha.png', mode='wb') as file:
        file.write(res.content)


def get_headers(url):
    """Makes a headers dict for the session"""
    return {
        'referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

def send_req(url, session):
    """Sends the request to make a vote"""
    # get webpage
    res = session.get(url)
    # scrap webpage
    get_captcha(session)
    payload = get_payload(res)
    # needed to bypass referer and webscrape detector
    headers = get_headers(url)
    session.headers.update(headers)
    # send post to make a vote
    res = session.post(url, data=payload)

    return len(res.content) > 100


def make_sync_request(url, total_req=1):
    """Sends requests until all required requests are successful"""
    success, req_sended = 0, 0
    with requests.session() as session:
        while success < total_req:
            if send_req(url, session):
                success += 1

            req_sended += 1
            
        print('Success rate: {}% ({}/{})'.format(success * 100  / req_sended, success, req_sended))


# 0: invalid id
# 5: Wrong key value
# 6: not keywas sended
# 7: Wrong referer
# 9: No scripts allowed, you need to be human
# 11: bad captcha
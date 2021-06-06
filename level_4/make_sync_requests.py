import requests
from bs4 import BeautifulSoup
from Proxy_List_Scrapper import Scrapper

def get_proxies():
    """Featches a random list of proxies"""
    scrapper = Scrapper(category='ALL', print_err_trace=False)
    data = scrapper.getProxies()

    proxies = []
    for item in data.proxies:
        proxies.append('{}:{}'.format(item.ip, item.port))
    return proxies


def send_request(url, proxy):
    """Sends a get request to scrape a website and
    then sends a post request to make a vote"""
    succeded = False
    try:
        session = requests.Session()
        session.proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }

        res = session.get(url, timeout=5)
        # scrap webpage
        soup = BeautifulSoup(res.text, 'html.parser')
        form = soup.form
        key_input = form.find('input', {'name': 'key'})

        payload = {
            'id': '2829',
            'holdthedoor': 'Submit',
            'key': key_input['value']
        }

        # needed to bypass referer and webscrape detector
        session.headers.update({
            'referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })

        res = session.post(url, data=payload, timeout=5)
        if len(res.text) > 100:
            succeded = True
        session.close()
    except:
        print('An error occured')

    return succeded


def make_sync_request(url, total_req=1):
    """Handles the http requests"""
    ind, success, sended_req = 0, 0, 0
    proxies = get_proxies()

    while success < total_req and ind < len(proxies):
        proxy = proxies[ind]
        if send_request(url, proxy):
            print('Sucess!!')
            success += 1

        ind += 1
        if ind == len(proxies):
            ind, proxies = 0, get_proxies()
        
        sended_req += 1

    print('Success rate: {}% ({}/{})'.format(success * 100/ sended_req, success, sended_req))

# 0: invalid id
# 5: Wrong key value
# 6: not keywas sended
# 7: Wrong referer
# 9: No scripts allowed, you need to be human
# 11: bad captcha
# 12: already voted!

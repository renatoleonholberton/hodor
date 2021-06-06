"""This module contains functions to make synchronous http requests"""
import requests
from bs4 import BeautifulSoup

def get_payload(res):
    """Generates the payload needed to be send"""
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.form
    key_input = form.find('input', {'name': 'key'})

    return {
        'id': '2829',
        'holdthedoor': 'Submit',
        'key': key_input['value']
    }


def send_request(url, session):
    """Sends the requests to make one vote"""
    res = session.get(url)
    payload = get_payload(res)
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

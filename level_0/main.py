"""This module http makes requests to vote 1024 times for an id"""
import time
start_requests = __import__('async_requests').start_requests

url = 'http://158.69.76.135/level0.php'

if __name__ == '__main__':
    start = time.time()

    start_requests(url, 1024)

    print('elapsed time:', time.time() - start)

"""This module http makes requests to vote 4096 times for an id"""
import time
start_sync_requests = __import__('sync_requests').make_sync_request
start_async_requests = __import__('async_requests').start_requests

url = 'http://158.69.76.135/level1.php'

if __name__ == '__main__':
    start = time.time()

    start_sync_requests(url, 513)
    # start_async_requests(url, 4096)

    print('elapsed time:', time.time() - start)

"""This modules executes code that makes 1024 successsful 
votes for an in"""
import time
make_sync_request = __import__('make_sync_requests').make_sync_request

url = 'http://158.69.76.135/level3.php'

if __name__ == '__main__':
    start = time.time()

    make_sync_request(url, 1024)

    print('elapsed time:', time.time() - start)

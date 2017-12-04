import hmac
import hashlib
import json
import random
import urllib
import time
from httplib import HTTPSConnection


host = 'cdn.api.qcloud.com'
https_client = HTTPSConnection(host)
url='/v2/index.php'
msg = ''


class ResponseException(Exception):
    pass


def get_signature(msg, key="rQJWruHt9yb3D8docqMlDHorvMACItDS"):
    return urllib.urlencode({'Signature':hmac.new(key, msg, hashlib.sha1).digest().encode('base64').rstrip()})


def get_url(args_str, host='cdn.api.qcloud.com', url='/v2/index.php'):
    """
    :param args_str:
    :param url:
    :param host:
    :rtype: basestring
    """
    signature_src = 'GET' + host + url + '?' + args_str
    request_url = url + '?' + args_str + '&' + get_signature(signature_src)
    return request_url


def get_args_str(path, task_id=None, dst=None):
    args = json.load(open(path))
    args['Nonce'] = random.randint(0, 2147483647)
    args['Timestamp'] = int(time.time())
    print args['Nonce'], args['Timestamp']
    if id is not None:
        args['taskId'] = task_id
    if dst is not None:
        args['urlInfos.0'] = dst
    args_str = "&".join(sort_args(args))
    return args_str


def sort_args(args):
    arg_tuples = sorted(args.iteritems(), key=lambda x: x[0])
    sorted_args = []
    for arg in arg_tuples:
        sorted_args.append('{k}={v}'.format(k=arg[0], v=arg[1]))
    return sorted_args


def check_progress(connect, request_url):
    connect.request('GET', request_url)
    response = json.loads(https_client.getresponse().read())
    return response


def go(dst=None):
    try:
        warm_up_args_str = get_args_str('warm_up_args.json', dst=dst)
        warm_up_request_url = get_url(warm_up_args_str, host, url)
        https_client.request('GET', warm_up_request_url)
        warm_up_response = json.loads(https_client.getresponse().read())
        print warm_up_response
        if warm_up_response['code'] == 0:
            taskId = warm_up_response['data']['taskId']
            print taskId
        else:
            msg = warm_up_response['message']
            raise ResponseException

        while True:
            get_status_args_str = get_args_str('get_status_args.json', task_id=taskId)
            get_status_request_url = get_url(get_status_args_str, host, url)
            progress_response = check_progress(https_client, get_status_request_url)
            print progress_response
            if progress_response['code'] != 0:
                msg = progress_response['message']
                raise ResponseException
            print 'Progress: {0}% accomplished'.format(progress_response['data']['progress'])
            if progress_response['data']['status'] == 'done':
                print 'Done'
                return True, 'Done'
                break
            time.sleep(1)
    except Exception, e:
        print u'Exception: {exception}, message: {msg}'.format(exception=str(e), msg=msg)
        return False, msg


if __name__ == '__main__':
    go()

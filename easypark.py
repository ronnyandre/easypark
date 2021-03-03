import requests
import json
import time
import pathlib

# authentication variables
username = None
password = None
user_id = None

# define the base url
def _url(path):
    return 'https://easypark.no/api/b2c/' + path

def _checkfile(file='cookies.txt'):
    # get file path
    fp = pathlib.Path(file)
    
    # check if file exists
    if (fp.is_file() == False):
        # create file
        open(file, 'w').close()
    
    return True

# authenticate the api
def authenticate():
    # empty cookie file
    empty_cookiefile()

    # set body
    body = {
        'redirectUrl': '/parking/no',
        'userName': username,
        'password': password
    }

    # post data to endpoint
    response = requests.post(_url('login/auth'), json=body)

    # if not successful
    if response.status_code != 200:
        raise Exception('POST /login/auth/ {}'.format(response.status_code))

    # get cookies
    cookies = response.cookies.get_dict()

    # save cookies for later
    with open('cookies.txt', 'w') as f:
        json.dump(cookies, f)
    
    # return json response
    return response.json() 

# list latest parkings
def list_parkings(pagesize = 10, page = 0):
    # set body
    body = {
        'filterData': {
            'pageSize': pagesize,
            'page': page
        },
        'parkingUserId': user_id
    }
    
    # read cookies from file
    f = open('cookies.txt', 'r')
    cookies = f.read()

    # if cookie file is empty
    if len(cookies) == 0:
        # re-authenticate
        authenticate()

    # post request
    response = requests.post(_url('parking/list'), json=body, cookies=json.loads(cookies))
    
    # if access is forbidden
    if response.status_code == 401:
        # re-authenticate
        authenticate()
        # post new request
        response = requests.post(_url('parking/list'), json=body, cookies=json.loads(cookies))
    
    
    # if response is not ok
    if response.status_code != 200:
        list_parkings( pagesize, page )
        # show error message
        #raise Exception('POST /parking/list/ {}'.format(response.status_code))

    # return json response
    return response.json()

# empty cookie file
def empty_cookiefile():
    open('cookies.txt', 'w').close()

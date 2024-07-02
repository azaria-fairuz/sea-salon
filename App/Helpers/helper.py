from configparser import ConfigParser
import os, psycopg2, requests

base_dir = os.getcwd()
database_url = 'postgresql://azaria:K51794kKiQ2OtvwNDp69-w@azaria-cluster-7081.6xw.aws-ap-southeast-1.cockroachlabs.cloud:26257/sea-salon?sslmode=verify-full' # for development ONLY!

def get_curr_work_dir():
    directories = dict()

    directories['templates_dir'], directories['public_dir'] = os.path.join(base_dir, 'App/Views/'), os.path.join(base_dir, 'Public')
    directories['controllers_dir'], directories['helpers_dir'] = os.path.join(base_dir, 'App/Controllers'), os.path.join(base_dir, 'App/Helpers')
    directories['modules_dir'] = os.path.join(base_dir, 'Modules')

    return directories

def connect(url=database_url):
    try:
        with psycopg2.connect(url) as conn:
            # print('Connected to the PostgreSQL server')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def make_requests(url, method, querystring=None, headers=None):
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=querystring)
    return response.json()
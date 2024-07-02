from configparser import ConfigParser
import os, psycopg2, requests

base_dir = os.getcwd()

def load_config(filename=f'{base_dir}/config.ini', section='DATABASE'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def get_curr_work_dir():
    directories = dict()

    directories['templates_dir'], directories['public_dir'] = os.path.join(base_dir, 'App/Views/'), os.path.join(base_dir, 'Public')
    directories['controllers_dir'], directories['helpers_dir'] = os.path.join(base_dir, 'App/Controllers'), os.path.join(base_dir, 'App/Helpers')
    directories['modules_dir'] = os.path.join(base_dir, 'Modules')

    return directories

def connect():
    url = load_config()['database_url']
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

def has_empty_value(list_data):
    if ('' in list_data) or (None in list_data):
        return True
    else:
        return False
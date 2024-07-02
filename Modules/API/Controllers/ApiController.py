import os, sys

sys.path.append(os.getcwd())
from App.Helpers.helper import connect, make_requests, has_empty_value
from flask import session
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from configparser import ConfigParser

base_url_api = '127.0.0.1:5000/api'

def authenticate(email, password):
    if (email != '' and password != ''):
        connection = connect()
        query = f'select "id", "name", "role", "email" from "user"."data" where "email" = \'{email}\' and "password" = crypt(\'{password}\', "password");'

        with connection.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()

        if len(data) != 0:
            access_token = create_access_token(identity=data[0][3])
            refresh_token = create_refresh_token(identity=data[0][3])

            session['user_id'] = data[0][0]
            session['user_name'] = data[0][1]
            session['user_role'] = data[0][2]
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token

            response = {'access_token':access_token, 'refresh_token':refresh_token}
        else:
            response = 'Email or Password is not recognized!'
    else:
        response = 'Email or Password must be entered!'

    return response

def remove_authentication(user_id, user_name, user_role, access_token, refresh_token):
    session.pop(user_id, None)
    session.pop(user_name, None)
    session.pop(user_role, None)
    session.pop(access_token, None)
    session.pop(refresh_token, None)

    return 'Successfully Logging Out!'
    
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = {'access_token':access_token}
    
    return response

def get_reviews(user_id=None):
    if user_id == None:
        query = f'select user_data."name" as username, salon_services."service", salon_branch."name" as branch_name, reviews."rating", reviews."notes" from "user"."reviews" as reviews join "salon"."services" as salon_services on reviews.service_id = salon_services.id join "salon"."branches" as salon_branch on reviews.branch_id = salon_branch.id join "user"."data" as user_data on reviews.user_id = user_data.id;'
    else:
        query = f'select user_data."name" as username, salon_services."service", salon_branch."name" as branch_name, reviews."rating", reviews."notes" from "user"."reviews" as reviews join "salon"."services" as salon_services on reviews.service_id = salon_services.id join "salon"."branches" as salon_branch on reviews.branch_id = salon_branch.id join "user"."data" as user_data on reviews.user_id = user_data.id where reviews.user_id = \'{user_id}\';'
    
    connection = connect()
    with connection.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    
    response = [{'name':response[0], 'service':response[1], 'branch':response[2], 'rating':int(response[3]), 'notes':response[4]} for response in data]

    return response

def add_reviews(user_id, service_id, branch_id, rating, notes):
    try:
        connection = connect()
        query_id = f'select id from "user"."reviews" order by id desc limit 1;'
        with connection.cursor() as cur:
            cur.execute(query_id)
            id = cur.fetchall()
            id = str(int(id[0][0]) + 1)

            query_reviews = """insert into "user".reviews(id, user_id, service_id, branch_id, rating, notes) values (%s, %s, %s, %s, %s, %s);"""
            cur.execute(query_reviews, (id, user_id, service_id, branch_id, rating, notes))

            connection.commit()

        response = 'Successfully Added New Reviews!'
        return response
    except Exception as e:
        connection.rollback()
        response = str(e)
        return response

def get_braches():
    connection = connect()
    query = f'select * from "salon"."branches";'

    with connection.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    
    response = [{'id':response[0], 'branch_name':response[1], 'branch_address':response[2], 'branch_open':str(response[3]), 'branch_close':str(response[4])} for response in data]
    return response

def get_services(branch_id):
    connection = connect()
    query = f'select "id", "service" from "salon"."services" where branch_id = \'{branch_id}\';'

    with connection.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    
    response = [{'id':response[0], 'service':response[1]} for response in data]
    return response

def get_reservation(user_id=None):
    connection = connect()
    if user_id == None:
        query = f'select user_data."name", user_data."phone", salon_service."service", salon_branch."name" as branch_name, reservation."date", reservation."status" from "salon"."reservations" as reservation join "user"."data" as user_data on user_data.id = reservation.user_id join "salon"."services" as salon_service on salon_service.id = reservation.service_id join "salon"."branches" as salon_branch on salon_branch.id = salon_service.branch_id order by reservation."date" asc;'
    else:
        query = f'select user_data."name", user_data."phone", salon_service."service", salon_branch."name" as branch_name, reservation."date", reservation."status" from "salon"."reservations" as reservation join "user"."data" as user_data on user_data.id = reservation.user_id join "salon"."services" as salon_service on salon_service.id = reservation.service_id join "salon"."branches" as salon_branch on salon_branch.id = salon_service.branch_id where reservation.user_id = \'{user_id}\' order by reservation."date" asc;'

    with connection.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    
    response = [{'user_name':response[0], 'user_phone':response[1], 'service':response[1], 'branch':response[1], 'date':str(response[1]), 'status':response[1]} for response in data]
    return response

def add_reservation(user_id, phone, service_id, date):
    try:
        connection = connect()
        query_id = f'select id from "salon"."reservations" order by id desc limit 1;'
        with connection.cursor() as cur:
            cur.execute(query_id)
            id = cur.fetchall()

            # construct id
            split_id = list(id[0][0])
            id_str, id_int  = ''.join(split_id[:4]), ''.join(split_id[4:])
            id = f'{id_str}{int(id_int) + 1:0{len(id_int)}d}'

            # there is no need to check date since it is unique and difference is only 1 hour
            query_reservation = """insert into "salon"."reservations"(id, user_id, phone, service_id, date, status) values (%s, %s, %s, %s, %s, %s);"""
            cur.execute(query_reservation, (id, user_id, phone, service_id, date, 0))

            connection.commit()

        response = 'Successfully Created a Reservation!'
        return response
    except Exception as e:
        connection.rollback()
        response = str(e)
        return response
    
def add_services(service, branch_id):
    try:
        # check user's role
        user_role = session.get('user_role', 'Guest')
        if user_role != 'Admin':
            response = 'Cannot add services due to the lack of current authorization!'
            return response
        
        connection = connect()
        query_id = f'select id from "salon"."services" where branch_id = \'{branch_id}\' order by id desc limit 1;'
        with connection.cursor() as cur:
            cur.execute(query_id)
            id = cur.fetchall()

            # construct id
            if len(id) != 0:
                split_id = list(id[0][0])
                id_branch, id_branch_number, id_service = ''.join(split_id[:4]), ''.join(split_id[4:8]), ''.join(split_id[8:])
                id = f'{id_branch}{id_branch_number}{int(id_service) + 1:0{len(id_service)}d}'
            else:
                id = f'{branch_id}0001'

            query_service = """insert into "salon"."services"(id, service, branch_id) values (%s, %s, %s);"""
            cur.execute(query_service, (id, service, branch_id))

            connection.commit()

        response = 'Successfully Added New Services!'
        return response
    except Exception as e:
        connection.rollback()
        response = str(e)
        return response

def add_branch(name, address, open, close, time_zone):
    try:
        # check user's role
        user_role = session.get('user_role', 'Guest')
        if user_role != 'Admin':
            response = 'Cannot add branch due to the lack of current authorization!'
            return response
        
        connection = connect()
        query_id = f'select id from "salon"."branches" order by id desc limit 1;'
        with connection.cursor() as cur:
            cur.execute(query_id)
            id = cur.fetchall()

            # construct id
            split_id = list(id[0][0])
            id_str, id_int  = ''.join(split_id[:4]), ''.join(split_id[4:])
            id = f'syst{int(id_int) + 1:0{len(id_int)}d}'

            query_branch = """insert into "salon".branches(id, name, address, open, close, time_zone) values (%s, %s, %s, %s, %s, %s);"""
            cur.execute(query_branch, (id, name, address, open, close, time_zone))

            connection.commit()

        response = 'Successfully Added New Branch!'
        return response
    except Exception as e:
        connection.rollback()
        response = str(e)
        return response

def add_users(name, email, phone, password, role):
    try:
        # validate required data
        if (has_empty_value([name, email, password, role])):
            response = 'All required data must be filled!'
            return response
        
        connection = connect()
        
        # assuming that thare are only 2 roles
        query_id = f'select id from "user"."data" order by id desc limit 1;'
        with connection.cursor() as cur:
            cur.execute(query_id)
            id = cur.fetchall()

            # construct id
            split_id = list(id[0][0])
            id_str, id_int  = 'cstr', ''.join(split_id[4:])
            id = f'{id_str}{int(id_int) + 1:0{len(id_int)}d}'

            query_user = f'insert into "user"."data"(id, name, email, phone, password, role) values (\'{id}\', \'{name}\', \'{email}\', \'{phone}\', crypt(\'{password}\', gen_salt(\'md5\')), \'{role}\');'
            cur.execute(query_user)

            connection.commit()

        response = 'Successfully Added New User!'
        return response
    except Exception as e:
        connection.rollback()
        response = str(e)
        return response
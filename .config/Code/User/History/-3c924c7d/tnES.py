'''
=============================================
========== Data Management Systems ==========
============== LECD 2023/2024 ===============
=============================================
=================== Demo ====================
=============================================
=============================================
=== Department of Informatics Engineering ===
=========== University of Coimbra ===========
=============================================

Authors: 
  Nuno Antunes <nmsa@dei.uc.pt>
  João R. Campos <jrcampos@dei.uc.pt>
  Updated on 10/2022 by Bruno Cabral <bcabral@dei.uc.pt>  
  University of Coimbra

How to run?
$ python3 -m venv django_env
$ source django_env/bin/activate
$ pip3 install flask
$ pip3 install psycopg2-binary
$ python3 demo-api.py
--> Ctrl+C to stop
$ deactivate
'''

import flask
import logging
import psycopg2
import time

app = flask.Flask(__name__)

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    # connection details should not be here, especially the password
    db = psycopg2.connect(
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
        database='labclassdata'
    )

    return db


'''

--------------------- Endpoints

'''

@app.route('/') 
def landing_page():
    return '''
        REST API Landing Page <br/><br/>
        Check the sources for instructions on how to use the endpoints<br/><br/>
        SGD 2022<br/><br/>
    '''


##
## Demo GET
##
## Obtain all departments in JSON format
##
## To use it, access: 
## 
## http://localhost:8080/departments/
##

@app.route('/departments/', methods=['GET'], strict_slashes=True)
def get_all_departments():
    logger.info('GET /departments')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT dept_name, building, budget FROM department')
        rows = cur.fetchall()

        logger.debug('GET /departments - parse')
        Results = []
        for row in rows:
            logger.debug(row)
            content = {'Department': row[0], 'Building': row[1], 'Budget': row[2]}
            Results.append(content)  # appending to the payload to be returned

        response = {'status': StatusCodes['success'], 'results': Results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /departments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


##
## Demo GET
##
## Obtain department with dept_name <dept_name>
##
## To use it, access: 
## 
## http://localhost:8080/departments/physics
##

@app.route('/departments/<dept_name>', methods=['GET'])
def get_department(dept_name):
    logger.info('GET /departments/<dept_name>')

    logger.debug(f'dept_name: {dept_name}')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT dept_name, building, budget FROM department where lower(dept_name) like lower(%s)', (dept_name,))
        rows = cur.fetchall()

        row = rows[0]

        logger.debug('GET /departments/<dept_name> - parse')
        logger.debug(row)
        content = {'Department': row[0], 'Building': row[1], 'Budget': row[2]}

        response = {'status': StatusCodes['success'], 'results': content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /departments/<dept_name> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


##
## Demo POST
##
## Add a new department in a JSON payload
##
## To use it, you need to use postman or curl: 
##
## curl -X POST http://localhost:8080/departments/ -H 'Content-Type: application/json' -d '{"dept_name": "Engineering", "budget": "70000", "building": "Socrates"}'
##

@app.route('/departments/', methods=['POST'])
def add_departments():
    logger.info('POST /departments')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /departments - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
    if 'dept_name' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'dept_name value not in payload'}
        return flask.jsonify(response)

    # parameterized queries, good for security and performance
    statement = 'INSERT INTO department (dept_name, building, budget) VALUES (%s, %s, %s)'
    values = (payload['dept_name'], payload['building'], payload['budget'])

    try:
        cur.execute(statement, values)

        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Inserted dep {payload["dept_name"]}'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /departments - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


##
## Demo PUT
##
## Update a department based on a JSON payload
##
## To use it, you need to use postman or curl: 
##
## curl -X PUT http://localhost:8080/departments/<dept_name> -H 'Content-Type: application/json' -d '{"budget": "5000"}'
##

@app.route('/departments/<dept_name>', methods=['PUT'])
def update_departments(dept_name):
    logger.info('PUT /departments/<dept_name>')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'PUT /departments/<dept_name> - payload: {payload}')

    # do not forget to validate every argument, e.g.,:
    if 'budget' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'budget is required to update'}
        return flask.jsonify(response)

    # parameterized queries, good for security and performance
    statement = 'UPDATE department SET budget = %s WHERE upper(dept_name) like upper(%s)'
    values = (payload['budget'], dept_name)

    try:
        res = cur.execute(statement, values)
        response = {'status': StatusCodes['success'], 'results': f'Updated: {cur.rowcount}'}

        # commit the transaction
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


if __name__ == '__main__':
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8089
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')

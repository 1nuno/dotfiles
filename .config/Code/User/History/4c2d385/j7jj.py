import flask
import psycopg2
import logging


app = flask.Flask(__name__)

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

def db_connection():
    db = psycopg2.connect(
        user='postgres',
        password='password',
        host='localhost',
        port='5432',
        database='postgres'
    )

    return db





@app.route('/')
def landing_page():
    return '''
        REST API Landing Page <br/><br/>
        Check the sources for instructions on how to use the endpoints<br/><br/>
        SGD 2022<br/><br/>
        '''


def  verificar_payload(payload, *required_fields):
    for field in required_fields:
        if field not in payload:
            response = {'status': StatusCodes['api_error'], 'results': f'{field} value not in payload'}
            return flask.jsonify(response)
    return None

#Adicionar um ITEM
@app.route('/proj/api/items/', methods=['POST'])
def add_items():
    logger.info('POST /proj/api/items/')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /items - payload: {payload}')

    validation_result = verificar_payload(payload, 'name', 'category', 'price', 'stock','manufacturer','category','weight','image_url')

    if validation_result:
        return validation_result

    statement = ('INSERT INTO item (name,category_id,price,stock,description,manufacturer_id,weight,image_url,last_updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, CURRENT_TIMESTAMP)')

    values = (payload['name'], payload['category'], payload['price'],payload['stock'],payload['description'],payload['manufacturer'],payload['weight'],payload['image_url'])

    try:
        cur.execute(statement, values)


        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'],
            'results': f'Inserted item {payload["name"]}',
            'data': {
                "name": payload["name"],
                "category": payload['category'],
                "price": payload['price'],
                "stock": payload['stock'],
                "description": payload['description'],
                "manufacturer": payload['manufacturer'],
                "weight": payload['weight'],
                "image_url": payload['image_url']
            }
}


    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /items - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)




# Update de um Item

def definirPayload (payload,*fields):
    parameters = []
    values = []
    for field in fields:
        if field in payload:
            parameters.append(f'{field} = %s')
            values.append(payload[field])
    return ', '.join(parameters), values



@app.route('/proj/api/items/<id>', methods=['PUT'])
def update_items(id):
    logger.info('PUT /proj/api/items/<id>')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'PUT items/<item_id> - payload: {payload}')

    if 'id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'id value not in payload'}
        return flask.jsonify(response)

    parameters, values = definirPayload (payload,'name', 'category_id', 'price', 'stock', 'description', 'manufacturer','weight','image_url')

    if not parameters:
        response = {'status': StatusCodes['api_error'], 'results': 'no values to update'}
        return flask.jsonify(response)

    statement = f'UPDATE item SET {parameters}, last_updated = CURRENT_TIMESTAMP WHERE id = %s'
    values.append(payload['id'])
    try:
        res = cur.execute(statement, values)
        response = {'status': StatusCodes['success'], 'results': f'Item updated sucessfully', 
                    'data':{'id': payload['id']}}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)



# Delete Item From

@app.route('/proj/api/cart/<item_id>', methods=['DELETE'])
def delete_items(item_id):
    logger.info('DELETE proj/api/cart/<item_id>')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'DELETE cart/<item_id> - payload: {payload}')

    validation_result = verificar_payload(payload, 'cart_client_id','item_id')

    if validation_result:
        return validation_result

    statement = f'DELETE from cart_item WHERE item_id = %s and cart_client_id = %s'
    values = (payload['item_id'],payload['cart_client_id'])

    try:
        res = cur.execute(statement, values)
        response = {'status': StatusCodes['success'], 'results': f'Item removed from the shopping cart.','data':'null'}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


# Adicionar um ITEM a um carrinho


def verificarStock(quantity, item_id):
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(f'SELECT stock FROM item WHERE id={item_id}')
        stock = cur.fetchone()[0]

    except Exception as e:
        response = {'status': StatusCodes['api_error'], 'results': f'Database error: {str(e)}'}
        return flask.jsonify(response)
    finally:
        cur.close()
        conn.close()

    if stock < quantity:
        response = {'status': StatusCodes['api_error'], 'results': f'Quantidade máxima possível: {stock}'}
        return flask.jsonify(response)
    return None


@app.route('/proj/api/cart', methods=['POST'])
def add_cart_items():
    logger.info('POST /proj/api/cart')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /cart - payload: {payload}')

    validation_result = verificar_payload(payload, 'item_id','quantity','cart_client_id')
    if validation_result:
        return validation_result

    verificar_stock = verificarStock (payload['quantity'], payload['item_id'])
    if verificar_stock:
        return verificar_stock

    statement = ('INSERT INTO cart_item  (quantity,item_id,cart_client_id) VALUES (%s,%s,%s)')

    values = (payload['quantity'], payload['item_id'], payload['cart_client_id'])

    try:
        cur.execute(statement, values)

        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'Item added to the shopping cart.','data': 'null'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /items - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)




#Consultar detalhes de um item

@app.route('/proj/api/items/<id>', methods=['GET'])
def get_item(id):
    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(f'SELECT id,name,category_id,price,stock,description,manufacturer_id,weight,image_url FROM item WHERE id = {id}')
        rows = cur.fetchall()
        row = rows[0]

        logger.debug('GET /proj/api/items/<id> - parse')
        logger.debug(row)
        content = {'Id': row[0], 'Name': row[1], 'Category': row[2],'Price': row[3] ,'Stock': row[4],'Description':row[5],'Manufacturer':row[6],'Weight':row[7],'Image_url':row[8]}

        response = {'status': StatusCodes['success'], 'results': 'Item details retrieved successfully','data':content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /proj/api/items/<id> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)

#Pesquisar Item









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
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')
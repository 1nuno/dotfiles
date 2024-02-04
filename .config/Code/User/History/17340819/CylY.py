import flask
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from psycopg2 import sql

app = flask.Flask(__name__)
app.json.sort_keys = False

StatusCodes = {
    'success': '200 - success',
    'bad_request_error': '400 - bad request error',
    'api_error': '500 - api error'
}

def db_connection():
    conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432',
    database='postgres'
    )
    return conn


def insert_df_in_db(df, table):
    try:
        conn = db_connection()
        cur = conn.cursor()
        values = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        query  = "INSERT INTO %s (%s) VALUES %%s" % (table, cols)
        extras.execute_values(cur, query, values)
        conn.commit()
        print("Success")
    except (Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(error)
        conn.rollback()
        cur.close()
        print("Failure")
    finally:
        if conn is not None:
            conn.close()
        print('End')

##########################################################
## API
##########################################################
def verify_request_body(request_body, field_types, required_fields=[]):
    # duplicates in the request_body (its commented because postman takes care of this for us)
    # if len(list(request_body.keys())) != len(set(list(request_body.keys()))):
    #     response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be duplicate fields in your request body. Make sure to provide unique fields.'}
    #     return flask.jsonify(response)
    
    for field in request_body:
        if field not in field_types.keys():
            response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a problem with one of the column names you provided, more specifically: {field}.'}
            return flask.jsonify(response)

    for field in required_fields:
        if field not in request_body:
            response = {'status': StatusCodes['bad_request_error'], 'Error': f'Not enough information was provided. To insert an item its obligatory to provide the following information: {required_fields}'}
            return flask.jsonify(response)
        
    for field in request_body:
        if type(request_body[field]) != field_types[field]:
            response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
            return flask.jsonify(response)


@app.route('/') 
def landing_page():
    return '''
        REST API Landing Page <br/><br/>
        Check the sources for instructions on how to use the endpoints<br/><br/>
        SGD 2023<br/><br/>
    '''

# 1. Create Item (POST)
@app.route('/proj/api/items/', methods=['POST'])
def add_item():
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        required_fields = ["name",
                           "category_id",
                           "price",
                           "stock",
                           "manufacturer_id"]
        field_types = {"name":str,
                       "category_id":int,
                       "price":float,
                       "stock":int,
                       "manufacturer_id":int,
                       "description":str,
                       "weight":float,
                       "image_url":str}
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body
        cols = ','.join(list(request_body.keys()))
        query  = 'INSERT INTO item (%s) VALUES %%s' % cols
        cur.execute(query,(tuple(request_body.values()),))
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': f'Inserted item: {request_body["name"]}',
                    'data': request_body}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error)}
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 2. Update Item (PUT)
@app.route('/proj/api/items/<id>', methods=['PUT'])
def update_item(id):
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        field_types = {"name":str,
                       "category_id":int,
                       "price":float,
                       "stock":int,
                       "manufacturer_id":int,
                       "description":str,
                       "weight":float,
                       "image_url":str}
        is_broken_body = verify_request_body(request_body,field_types)
        if is_broken_body is not None:
            return is_broken_body
        vals = ','.join([f"{i}=%s" for i in request_body.keys()])
        query = ''' DO $$
                    BEGIN
                        UPDATE item SET %s WHERE id=%%s;
                        IF not found then RAISE EXCEPTION 'Item not found';
                        END IF;
                    END $$;''' % vals
        cur.execute(query,list(request_body.values()) + [id])
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': "Item updated successfully :).",
                    'data': request_body}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item you are trying to update doesn\'t exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error)}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 3. Delete Item from Shopping Cart (DELETE)
@app.route('/proj/api/cart/<item_id>', methods=['DELETE'])
def delete_items(item_id):
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''DO $$
                   BEGIN
                    DELETE from cart_item WHERE cart_client_id=\'client123\' AND item_id=%s;
                    if not found then RAISE EXCEPTION 'Item not found';
                    END IF;
                   END $$;'''
        cur.execute(query, (item_id,))
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': "Item removed from the shopping cart :|.",
                    'data': None}
        
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item you are trying to delete doesn\'t exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 4. Add Item to Shopping Cart (POST)
@app.route('/proj/api/cart', methods=['POST'])
def add_cart_item():
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        required_fields = ["item_id",
                           "quantity"]
        field_types = {"quantity":int,
                       "item_id":int}
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body
        cols = ','.join(list(request_body.keys())) + ',cart_client_id'
        vals = tuple(list(request_body.values()) + ['client123'])
        query = '''DO $$
                   DECLARE available_stock INTEGER;
                           itemId INTEGER := %(thisId)s;
                           thisQuantity INTEGER := %(thisQuantity)s;
                   BEGIN
                       SELECT stock FROM item WHERE item.id = itemId INTO available_stock;
                       
                       IF thisQuantity > available_stock THEN
                           RAISE EXCEPTION 'Not enough stock :(.';
                       END IF;

                       INSERT INTO cart_item (%(cols)s) VALUES %%s
                       ON CONFLICT (item_id, cart_client_id)
                       DO UPDATE SET quantity = cart_item.quantity + thisQuantity
                       WHERE cart_item.item_id = itemId AND cart_item.cart_client_id = 'client123';
                   END $$;''' % {"thisId":request_body['item_id'],
                                 "thisQuantity":request_body['quantity'],
                                 "cols":cols}
        cur.execute(query,(vals,))
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': f'Item added to the shopping cart :).',
                    'data': None}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.ForeignKeyViolation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item_id you provided doesn\'t exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error)}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 5. Get Items List (GET). 
@app.route('/proj/api/items', methods=['GET'])
def get_item_list():
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        field_types = {"page":int,
                       "limit":int,
                       "category":str,
                       "sort":str}
        is_broken_body = verify_request_body(request_body,field_types)
        if is_broken_body is not None:
            return is_broken_body

        if "page" in request_body:
            page = sql.Literal(str(request_body["page"]))
        else:
            page = sql.Identifier("page")

        if "limit" in request_body:
            limit = sql.Literal(str(request_body["limit"]))
        else:
            limit = sql.SQL("count(*) OVER ()")

        if "category" in request_body:
            category = sql.Literal(request_body["category"])
        else:
            category = (sql.Identifier("cat") + sql.Identifier("name")).join('.')

        if "sort" in request_body:
            sort = sql.Identifier(request_body["sort"])
        else:
            sort = sql.Identifier("ctid")

        query = sql.SQL(''' WITH items_sum AS (
                                        SELECT item_id, SUM(quantity) AS total_unit_sales
                                        FROM purchase_item
                                        GROUP BY item_id
                                      ),
                            final_output AS (
                                                SELECT item.id,
                                                       item.name,
                                                       cat.name AS category,
                                                       item.price,
                                                       item.stock,
                                                       item.description,
                                                       man.name AS manufacturer,
                                                       item.weight,
                                                       item.image_url,
                                                       CAST(COALESCE(itsum.total_unit_sales,0) AS INTEGER) AS total_unit_sales,
                                                       (ROW_NUMBER() OVER (ORDER BY "item".{}) - 1) / {} + 1 AS page
                                                FROM item
                                                FULL JOIN items_sum itsum ON itsum.item_id = item.id
                                                JOIN category cat ON cat.id = item.category_id
                                                JOIN manufacturer man ON man.id = item.manufacturer_id
                                                WHERE cat.name = {}
                                            )
                            SELECT * 
                            FROM final_output
                            WHERE page = {};''').format(sort,limit,category,page)
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = []
        cols = [desc[0] for desc in cur.description]
        for row in values:
            formated_row = {i:j for i,j in zip(cols,row)}
            data.append(formated_row)
        response = {'status': StatusCodes['success'],
                    'message': "Items retrieved successfully :).",
                    'data': data}
        
    except UnsupportedMediaType as error:
        query = ''' WITH items_sum AS (
                                        SELECT item_id, SUM(quantity) AS total_unit_sales
                                        FROM purchase_item
                                        GROUP BY item_id
                                      )
                    SELECT item.id,
                           item.name,
                           cat.name AS category,
                           item.price,
                           item.stock,
                           item.description,
                           man.name AS manufacturer,
                           item.weight,
                           item.image_url,
                           CAST(COALESCE(itsum.total_unit_sales,0) AS INTEGER) AS total_unit_sales,
                           (ROW_NUMBER() OVER (ORDER BY item.ctid) - 1) / count(*) OVER () + 1 AS page
                    FROM item
                    FULL JOIN items_sum itsum ON itsum.item_id = item.id
                    JOIN category cat ON cat.id = item.category_id
                    JOIN manufacturer man ON man.id = item.manufacturer_id
                    WHERE category_id = category_id;'''
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = []
        cols = [desc[0] for desc in cur.description]
        for row in values:
            formated_row = {i:j for i,j in zip(cols,row)}
            data.append(formated_row)
        response = {'data': data}
        return flask.jsonify(response)
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except IndexError as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item_id your providing doesnt exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 6. Get Item Details (GET) 
@app.route('/proj/api/items/<id>', methods=['GET'])
def get_item_details(id):
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = 'SELECT * FROM item WHERE id = %s'
        cur.execute(query,(id,))
        conn.commit()
        values = cur.fetchall()[0]
        cols = [desc[0] for desc in cur.description]
        data = {i:j for i,j in zip(cols,values)}
        response = {'status': StatusCodes['success'],
                    'message': "Item details retrieved successfully :).",
                    'data': data}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except IndexError as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item_id your providing doesnt exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 7. Search Items (GET)
@app.route('/proj/api/items/search', methods=['GET'])
def search_item():
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        field_types = {"param":str,
                       "search_by":str}
        required_fields = ["param"]
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body
        
        search_by = request_body.get("search_by","name")

        if search_by != "query":
            query = sql.SQL('SELECT * FROM item WHERE {}=%s').format(sql.Identifier(search_by))
            cur.execute(query,(request_body['param'],))
            conn.commit()

            values = cur.fetchall()
            data = []
            cols = [desc[0] for desc in cur.description]
            for row in values:
                formated_row = {i:j for i,j in zip(cols,row)}
                data.append(formated_row)
            response = {'status': StatusCodes['success'],
                        'message': "Items retrieved successfully :).",
                        'data': data}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except IndexError as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item_id your providing doesnt exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# 8. Get Top 3 Sales per Category (GET) 
@app.route('/proj/api/stats/sales', methods=['GET'])
def get_top3_sales_per_category():
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''WITH items_sum AS (
                    SELECT item_id, SUM(quantity) AS total_sales
                    FROM purchase_item
                    GROUP BY item_id
                ),
                grouped_data AS (
                    SELECT item.name as item_name, item.category_id, items_sum.total_sales
                    FROM items_sum
                    JOIN item ON items_sum.item_id = item.id
                ),
                ranked_grouped_data AS (
                    SELECT *,
                        ROW_NUMBER() OVER(PARTITION BY category_id ORDER BY total_sales DESC) AS item_rank
                    FROM grouped_data
                    LEFT JOIN category ON grouped_data.category_id = category.id
                )
                SELECT ranked_grouped_data.item_name, ranked_grouped_data.name as category_name, ranked_grouped_data.total_sales
                FROM ranked_grouped_data
                WHERE item_rank <= 3;'''
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = {"top_sales_per_category":{}}
        for item_name, category_name, total_sales in values:
            if category_name not in data['top_sales_per_category']:
                data['top_sales_per_category'][category_name] = [{"item_name":item_name,
                                                                  "total_sales":total_sales}]
            else:
                data['top_sales_per_category'][category_name].append({"item_name":item_name,
                                                                      "total_sales":total_sales})
        response = {'status': StatusCodes['success'],
                    'message': "Top 3 sales per category retrieved successfully :).",
                    'data': data}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


# 9. Purchase Items (POST) 
@app.route('/proj/api/purchase', methods=['POST'])
def make_a_purchase():
    try:
        conn = db_connection()
        cur = conn.cursor()
        request_body = flask.request.get_json()
        required_cart_fields = ["item_id",
                                "quantity"]
        field_cart_types = {"quantity":int,
                            "item_id":int}
        required_fields = ["cart",
                           "purchase_type",
                           "client_id"]
        field_types = {"cart":list,
                       "purchase_type":str,
                       "client_id":str}
        
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body

        quantities = ''
        itemIds = ''
        for r_b in request_body['cart']:
            is_broken_body = verify_request_body(r_b,field_cart_types,required_fields=required_cart_fields)
            if is_broken_body is not None:
                return is_broken_body
            quantities += str(r_b['quantity']) + ','
            itemIds += str(r_b['item_id']) + ','
        quantities = quantities.strip(',')
        itemIds = itemIds.strip(',')

        if request_body['purchase_type'] == 'aggregate':
            query = ''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION aggregate()
                        RETURNS purchase_info AS $$
                        DECLARE available_stock INTEGER;
                                itemIds INTEGER[];
                                quantities INTEGER[];
                                cart_quantity INTEGER;
                                purchase_price FLOAT;
                                most_recent_purchase_id INTEGER;
                                return_values purchase_info;
                                thisClient VARCHAR(50) := '%(clientId)s';
                        BEGIN
                            -- aggregate our json cart info to our cart_item
                            itemIds := ARRAY[%(itemIds)s];
                            quantities := ARRAY[%(quantities)s];
                            FOR i IN 1..array_length(itemIds, 1) LOOP
                                INSERT INTO cart_item (item_id,quantity,cart_client_id) VALUES (itemIds[i],quantities[i],thisClient)
                                ON CONFLICT (item_id, cart_client_id)
                                DO UPDATE SET quantity = cart_item.quantity + quantities[i]
                                WHERE cart_item.item_id = itemIds[i] 
                                AND   cart_item.cart_client_id = thisClient;


                                SELECT stock 
                                FROM item 
                                WHERE item.id = itemIds[i] 
                                INTO available_stock;

                                IF quantities[i] > available_stock THEN
                                    RAISE EXCEPTION 'Not enough stock :(.';
                                END IF;

                                SELECT quantity 
                                INTO cart_quantity
                                FROM cart_item 
                                WHERE item_id = itemIds[i] AND 
                                    cart_item.cart_client_id = thisClient;

                                UPDATE item 
                                SET stock = available_stock - cart_quantity
                                WHERE id = itemIds[i];
                            END LOOP;

                            -- compute the total purchase price into purchase_price
                            SELECT SUM(price*quantity) INTO purchase_price FROM item
                            JOIN cart_item ON item.id = cart_item.item_id
                            WHERE cart_item.cart_client_id = thisClient;
                            IF purchase_price IS NULL THEN
                                RAISE EXCEPTION 'Client ID not found.';
                            END IF;
                            
                            -- add the purchase info to purchase
                            INSERT INTO purchase (price, client_id) VALUES (purchase_price,thisClient);
                            
                            -- add the cart_item info into purchase_item
                            SELECT MAX(id) INTO most_recent_purchase_id FROM purchase WHERE client_id = thisClient;
                            INSERT INTO purchase_item (quantity, item_id, purchase_id)
                            SELECT ci.quantity, ci.item_id, most_recent_purchase_id
                            FROM cart_item ci
                            WHERE cart_client_id = thisClient;
                            
                            -- clear the cart_item
                            DELETE from cart_item WHERE cart_client_id = thisClient;

                            return_values.most_recent_purchase_id := most_recent_purchase_id;
                            return_values.purchase_price := purchase_price;
                            RETURN return_values;
                        END $$ LANGUAGE plpgsql;
                        SELECT aggregate();''' % {"quantities":quantities,
                                        "itemIds":itemIds,
                                        "clientId":request_body['client_id']}
        elif request_body['purchase_type'] == 'mixed':    
            query = ''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION mixed()
                        RETURNS purchase_info AS $$
                        DECLARE available_stock INTEGER;
                                itemIds INTEGER[] := ARRAY[%(itemIds)s];
                                quantities INTEGER[] := ARRAY[%(quantities)s];
                                prices NUMERIC[];
                                purchase_price FLOAT;
                                cart_quantity INTEGER;
                                thisClient VARCHAR(50) := '%(clientId)s';
                                most_recent_purchase_id INTEGER;
                                return_values purchase_info;
                        BEGIN
                            -- compute the total purchase price into purchase_price
                            SELECT SUM(prices_array * quantities_array) 
                            INTO purchase_price
                            FROM 
                            (SELECT unnest(ARRAY(
                                        SELECT price
                                        FROM item
                                        WHERE id = ANY(itemIds)))
                                    AS prices_array,
                                    unnest(quantities) 
                                    AS quantities_array)
                            AS prices_quantities;
                            
                            -- add the purchase info to purchase
                            INSERT INTO purchase (price, client_id) VALUES (purchase_price,thisClient);
                            
                            -- get the purchase id into most_recent_purchase_id
                            SELECT MAX(id) INTO most_recent_purchase_id FROM purchase WHERE client_id = thisClient;
                            
                            -- update the quantities in cart_item
                            FOR i IN 1..array_length(itemIds, 1) LOOP
                                SELECT stock 
                                FROM item 
                                WHERE item.id = itemIds[i] 
                                INTO available_stock;

                                IF quantities[i] > available_stock THEN
                                    RAISE EXCEPTION 'Not enough stock :(.';
                                END IF;

                                UPDATE item 
                                SET stock = available_stock - quantities[i]
                                WHERE id = itemIds[i];

                                SELECT quantity 
                                INTO cart_quantity
                                FROM cart_item 
                                WHERE item_id = itemIds[i] AND 
                                    cart_item.cart_client_id = thisClient;
                                
                                IF quantities[i] < cart_quantity THEN
                                    UPDATE cart_item 
                                    SET quantity = cart_quantity - quantities[i]
                                    WHERE item_id = itemIds[i] 
                                    AND   cart_client_id = thisClient;
                                ELSE
                                    DELETE FROM cart_item 
                                    WHERE cart_client_id = thisClient 
                                    AND   item_id = itemIds[i];
                                END IF;
                                
                                -- insert to purchase_item
                                INSERT INTO purchase_item (quantity, item_id, purchase_id)
                                VALUES (quantities[i], itemIds[i], most_recent_purchase_id);
                            END LOOP;
                            return_values.most_recent_purchase_id := most_recent_purchase_id;
                            return_values.purchase_price := purchase_price;
                            RETURN return_values;
                        END $$ LANGUAGE plpgsql;
                        SELECT mixed();''' % {"quantities":quantities,
                                      "itemIds":itemIds,
                                      "clientId":request_body['client_id']}
        elif request_body['purchase_type'] == 'individual':
            query = ''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION individual()
                        RETURNS purchase_info AS $$
                        DECLARE available_stock INTEGER;
                                itemIds INTEGER[] := ARRAY[%(itemIds)s];
                                quantities INTEGER[] := ARRAY[%(quantities)s];
                                purchase_price FLOAT;
                                thisClient VARCHAR(50) := '%(clientId)s';
                                most_recent_purchase_id INTEGER;
                                return_values purchase_info;
                        BEGIN
                            -- compute the total purchase price into purchase_price
                            SELECT SUM(prices_array * quantities_array) 
                            INTO purchase_price
                            FROM 
                            (SELECT unnest(ARRAY(
                                        SELECT price
                                        FROM item
                                        WHERE id = ANY(itemIds)))
                                    AS prices_array,
                                    unnest(quantities) 
                                    AS quantities_array)
                            AS prices_quantities;
                            
                            -- add the purchase info to purchase
                            INSERT INTO purchase (price, client_id) VALUES (purchase_price,thisClient);
                            
                            -- get the purchase id into most_recent_purchase_id
                            SELECT MAX(id) INTO most_recent_purchase_id FROM purchase WHERE client_id = thisClient;
                            
                            -- insert to purchase_item
                            FOR i IN 1..array_length(itemIds, 1) LOOP
                                SELECT stock 
                                FROM item 
                                WHERE item.id = itemIds[i] 
                                INTO available_stock;

                                IF quantities[i] > available_stock THEN
                                    RAISE EXCEPTION 'Not enough stock :(.';
                                END IF;

                                UPDATE item 
                                SET stock = available_stock - quantities[i]
                                WHERE id = itemIds[i];

                                INSERT INTO purchase_item (quantity, item_id, purchase_id)
                                VALUES (quantities[i], itemIds[i], most_recent_purchase_id);
                            END LOOP;

                            return_values.most_recent_purchase_id := most_recent_purchase_id;
                            return_values.purchase_price := purchase_price;
                            RETURN return_values;
                        END $$ LANGUAGE plpgsql;
                        SELECT individual();''' % {"quantities":quantities,
                                      "itemIds":itemIds,
                                      "clientId":request_body['client_id']}
        else:
            response = {'status': StatusCodes['bad_request_error'], 'Error': 'The purchase_type value is invalid, it must be one of the following 3: aggregate, mixed or individual.'}
            return response
        cur.execute(query)
        conn.commit()
        data = cur.fetchone()[0].strip('(').strip(')').split(',')
        response = {'status': StatusCodes['success'],
                    'message': f'Purchase successful. Order ID: {data[0]}',
                    'data': {
                        "order_id": int(data[0]),
                        "total_price": round(float(data[1]),2)
                    }}
    except psycopg2.errors.ForeignKeyViolation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'From the items you provided one of the following dont exist: item_id or client_id :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.InvalidTextRepresentation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided. Maybe you\'ve used a string where it should\'ve been an int?'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.SyntaxError as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        error_tip = str(error).split('\n')[0]
        response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a syntax error with the data you provided. {error_tip}'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        # NOTA para mim mesmo: Antes da entrega retirar os detalhes a mais do erro da response abaixo, so esta ai agora por motivos de teste.
        response = {'Error': f'An error ocurred - {type(error).__name__}', 'traceback': str(error)}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


if __name__ == '__main__':
    # Load data into the database
    # df = pd.read_csv('test_data.csv')
    # category = df.loc[:,['category']].rename(columns={"category": "name"}).drop_duplicates()
    # manufacturer = df.loc[:,['manufacturer']].rename(columns={"manufacturer": "name"}).drop_duplicates()
    # item = df.loc[:,['name',
    #       'price',
    #       'stock',
    #       'description',
    #       'weight',
    #       'image_url']]
    # item['manufacturer_id'] = pd.factorize(df['manufacturer'])[0] + 1
    # item['category_id'] = pd.factorize(df['category'])[0] + 1
    # client = df[~df['client_id'].isnull()].loc[:,['client_id',
    #                                               'client_name',
    #                                               'client_email']].rename(columns={"client_id": "id",
    #                                                                                "client_name": "name",
    #                                                                                "client_email": "email"}).drop_duplicates()
    # cart = df[~df['client_id'].isnull()].loc[:,['client_id']].drop_duplicates()
    # purchase = df.sort_values(by=['purchase_date'])[~df['purchase_date'].isnull()].loc[:,['purchase_date','client_id','price','purchase_quantity']]
    # purchase['id'] = [0,1,2,3]
    # purchase['price'] = purchase['price']*purchase['purchase_quantity']
    # purchase = purchase[['id','purchase_date','price','client_id']]
    # purchase_item = df.sort_values(by=['purchase_date'])[~df['purchase_date'].isnull()].loc[:,['purchase_quantity','item_id']]
    # purchase_item['id_purchase'] = [0,1,2,3]
    # purchase_item = purchase_item[['purchase_quantity','id_purchase','item_id']].rename(columns={"purchase_quantity":"quantity","id_purchase": "purchase_id"})

    # table_dfs = [category,manufacturer,item,client,cart,purchase,purchase_item]
    # table_names = ['category','manufacturer','item','client','cart','purchase','purchase_item']
    # for df,name in zip(table_dfs,table_names):
    #     insert_df_in_db(df, name)

    # run the app
    app.run(host='127.0.0.1', debug=True, threaded=True, port=8089)

import flask
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from psycopg2 import sql
import datetime

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

def create_tables():
    try:
        conn = db_connection()
        cur = conn.cursor()
        query  = '''DROP TABLE IF EXISTS item CASCADE;
                    CREATE TABLE item (
                        id		 BIGSERIAL,
                        name		 VARCHAR(50) NOT NULL,
                        price		 FLOAT(8) NOT NULL,
                        stock		 BIGINT NOT NULL,
                        description	 VARCHAR(512),
                        weight		 FLOAT(5),
                        image_url	 VARCHAR(150),
                        last_updated	 TIMESTAMP NOT NULL,
                        manufacturer_id BIGINT NOT NULL,
                        category_id	 BIGINT NOT NULL,
                        PRIMARY KEY(id)
                    );

                    DROP TABLE IF EXISTS client CASCADE;
                    CREATE TABLE client (
                        id		 VARCHAR(512),
                        name	 VARCHAR(100) NOT NULL,
                        email	 VARCHAR(50),
                        last_updated TIMESTAMP NOT NULL,
                        PRIMARY KEY(id)
                    );

                    DROP TABLE IF EXISTS cart CASCADE;
                    CREATE TABLE cart (
                        created	 TIMESTAMP NOT NULL,
                        client_id VARCHAR(512),
                        PRIMARY KEY(client_id)
                    );

                    DROP TABLE IF EXISTS purchase CASCADE;
                    CREATE TABLE purchase (
                        id		 BIGSERIAL,
                        purchase_date TIMESTAMP NOT NULL,
                        price	 FLOAT(8) NOT NULL,
                        client_id	 VARCHAR(512) NOT NULL,
                        PRIMARY KEY(id)
                    );

                    DROP TABLE IF EXISTS category CASCADE;
                    CREATE TABLE category (
                        id		 BIGSERIAL,
                        name	 VARCHAR(100) NOT NULL,
                        last_updated TIMESTAMP NOT NULL,
                        PRIMARY KEY(id)
                    );

                    DROP TABLE IF EXISTS manufacturer CASCADE;
                    CREATE TABLE manufacturer (
                        id		 BIGSERIAL,
                        name	 VARCHAR(512) NOT NULL,
                        last_updated TIMESTAMP NOT NULL,
                        PRIMARY KEY(id)
                    );

                    DROP TABLE IF EXISTS cart_item CASCADE;
                    CREATE TABLE cart_item (
                        quantity	 INTEGER NOT NULL,
                        item_id	 BIGINT,
                        cart_client_id VARCHAR(512),
                        PRIMARY KEY(item_id,cart_client_id)
                    );

                    DROP TABLE IF EXISTS purchase_item CASCADE;
                    CREATE TABLE purchase_item (
                        quantity	 BIGINT,
                        purchase_id BIGINT,
                        item_id	 BIGINT,
                        PRIMARY KEY(quantity,purchase_id,item_id)
                    );

                    ALTER TABLE item ADD CONSTRAINT item_fk1 FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id);
                    ALTER TABLE item ADD CONSTRAINT item_fk2 FOREIGN KEY (category_id) REFERENCES category(id);
                    ALTER TABLE cart ADD CONSTRAINT cart_fk1 FOREIGN KEY (client_id) REFERENCES client(id);
                    ALTER TABLE purchase ADD CONSTRAINT purchase_fk1 FOREIGN KEY (client_id) REFERENCES client(id);
                    ALTER TABLE category ADD UNIQUE (name);
                    ALTER TABLE manufacturer ADD UNIQUE (name);
                    ALTER TABLE cart_item ADD CONSTRAINT cart_item_fk1 FOREIGN KEY (item_id) REFERENCES item(id);
                    ALTER TABLE cart_item ADD CONSTRAINT cart_item_fk2 FOREIGN KEY (cart_client_id) REFERENCES cart(client_id);
                    ALTER TABLE purchase_item ADD CONSTRAINT purchase_item_fk1 FOREIGN KEY (purchase_id) REFERENCES purchase(id);
                    ALTER TABLE purchase_item ADD CONSTRAINT purchase_item_fk2 FOREIGN KEY (item_id) REFERENCES item(id);

                    ALTER TABLE item ALTER COLUMN last_updated SET DEFAULT now();
                    ALTER TABLE cart ALTER COLUMN created SET DEFAULT now();
                    ALTER TABLE purchase ALTER COLUMN purchase_date SET DEFAULT now();
                    ALTER TABLE category ALTER COLUMN last_updated SET DEFAULT now();
                    ALTER TABLE manufacturer ALTER COLUMN last_updated SET DEFAULT now();
                    ALTER TABLE client ALTER COLUMN last_updated SET DEFAULT now();

                    ALTER TABLE item ADD CONSTRAINT nonnegative_stock CHECK (stock >= 0);
                    ALTER TABLE item ADD CONSTRAINT positive_price CHECK (price > 0);
                    ALTER TABLE purchase_item ADD CONSTRAINT nonnegative_quantity CHECK (quantity >= 0);
                    ALTER TABLE cart_item ADD CONSTRAINT nonnegative_quantity CHECK (quantity >= 0);
                    
                    DROP PROCEDURE IF EXISTS check_stock;
                    CREATE PROCEDURE check_stock(item_id INTEGER, quantity INTEGER)
                    AS $$
                    DECLARE
                        available_stock INTEGER;
                    BEGIN
                        SELECT stock 
                        FROM item 
                        WHERE id = item_id 
                        INTO available_stock;
                        
                        IF quantity > available_stock THEN
                            RAISE EXCEPTION 'Not enough stock for item of id: % :(', item_id;
                        END IF;
                    END;
                    $$ LANGUAGE plpgsql;
                    
                    DROP PROCEDURE IF EXISTS add_or_append_to_cart;
                    CREATE OR REPLACE PROCEDURE add_or_append_to_cart(itemId INTEGER, thisQuantity INTEGER, thisClient VARCHAR(50))
                    AS $$
                    DECLARE cart_exists BOOLEAN;
                    BEGIN
                        SELECT EXISTS (
                        SELECT 1
                        FROM cart
                        WHERE client_id = thisClient) INTO cart_exists;
                        
                        IF cart_exists = FALSE THEN
                            INSERT INTO cart (client_id) VALUES (thisClient);
                        END IF;

                        INSERT INTO cart_item (item_id,quantity,cart_client_id) VALUES (itemId,thisQuantity,thisClient)
                        ON CONFLICT (item_id, cart_client_id)
                        DO UPDATE SET quantity = cart_item.quantity + thisQuantity
                        WHERE cart_item.item_id = itemId AND cart_item.cart_client_id = thisClient;
                    END;
                    $$ LANGUAGE plpgsql;
                    
                    DROP PROCEDURE IF EXISTS update_item_stock;
                    CREATE OR REPLACE PROCEDURE update_item_stock(itemId INTEGER, thisQuantity INTEGER)
                    AS $$
                    BEGIN
                        CALL check_stock(itemId, thisQuantity);
                        UPDATE item 
                        SET stock = stock - thisQuantity
                        WHERE id = itemId;
                    END;
                    $$ LANGUAGE plpgsql;
                    
                    DROP PROCEDURE IF EXISTS get_cart_item_quantity;
                    CREATE OR REPLACE PROCEDURE get_cart_item_quantity(IN itemId INTEGER, IN thisClient VARCHAR(50), OUT cart_quantity INTEGER)
                    AS $$
                    BEGIN
                        SELECT quantity 
                        INTO cart_quantity
                        FROM cart_item 
                        WHERE item_id = itemId AND 
                            cart_item.cart_client_id = thisClient;
                    END;
                    $$ LANGUAGE plpgsql;
                    
                    CREATE OR REPLACE FUNCTION update_item()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.last_updated := NOW();
                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;

                    DROP TRIGGER IF EXISTS update_item_last_updated on item;

                    CREATE TRIGGER update_item_last_updated
                    BEFORE UPDATE ON item
                    FOR EACH ROW
                    WHEN (NEW IS DISTINCT FROM OLD)
                    EXECUTE FUNCTION update_item();'''
        cur.execute(query)
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

def verify_request_body(request_body, field_types, required_fields=[]):
    for field in request_body:
        if field not in field_types:
            response = {'status': StatusCodes['bad_request_error'], 'Error': f'There seems to be a problem with one of the column names you provided, more specifically: {field}.'}
            return flask.jsonify(response)

    for field in required_fields:
        if field not in request_body:
            response = {'status': StatusCodes['bad_request_error'], 'Error': f'Not enough information was provided. To insert an item its obligatory to provide the following information: {required_fields}'}
            return flask.jsonify(response)
        
    for field in request_body:
        if type(request_body[field]) != field_types[field]:
            response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data types you provided.'}
            return flask.jsonify(response)
        
##########################################################
## API
##########################################################

@app.route('/') 
def landing_page():
    return '''
        REST API - Página inicial <br/><br/>
        Veja o relatório para instruções de como usar a api :).<br/><br/>
        Autores: Nuno - 2020242433 e Maria - <br/><br/>
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
                           "category",
                           "price",
                           "stock",
                           "manufacturer"]
        field_types = {"name":str,
                       "category":str,
                       "price":float,
                       "stock":int,
                       "manufacturer":str,
                       "description":str,
                       "weight":float,
                       "image_url":str}
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body
        
        cols = [sql.Identifier(i) for i in request_body.keys() if i not in ['manufacturer','category']]
        cols = sql.SQL(',').join(cols)
        values = [sql.Literal(j) for i,j in request_body.items() if i not in ['manufacturer','category']]
        values = sql.SQL(',').join(values)
        # query  = 'INSERT INTO item (%s) VALUES %%s' % cols
        query  = sql.SQL('''DO $$
                    DECLARE
                        cat_id INTEGER;
                        manu_id INTEGER;
                        cat VARCHAR(50) := {};
                        manu VARCHAR(50) := {};
                    BEGIN
                        SELECT id INTO cat_id
                        FROM category
                        WHERE name = cat;
                         
                        IF cat_id IS NULL THEN
                            RAISE EXCEPTION 'Invalid category: %.', cat;
                        END IF;
                        
                        SELECT id INTO manu_id
                        FROM manufacturer
                        WHERE name = manu;
                         
                        IF manu_id IS NULL THEN
                            RAISE EXCEPTION 'Invalid manufacturer: %.', manu;
                        END IF; 

                        INSERT INTO item (category_id,manufacturer_id,{})
                        VALUES (cat_id,manu_id,{});
                    END $$;''').format(sql.Literal(request_body['category']),
                                       sql.Literal(request_body['manufacturer']),
                                       cols,
                                       values)
        cur.execute(query)
        # cur.execute(query,(tuple(request_body.values()),))
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': f'Inserted item: {request_body["name"]}',
                    'data': request_body}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Don\'t worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure it\'s a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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

        if id.isnumeric():
            request_body = {'item_id':int(id)}
            field_types = {'item_id':int}
            is_broken_body = verify_request_body(request_body,field_types)
            if is_broken_body is not None:
                return is_broken_body
        else:
            return {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data type you provided.'}

        request_body = flask.request.get_json()
        field_types = {"name":str,
                       "category":str,
                       "price":float,
                       "stock":int,
                       "manufacturer":str,
                       "description":str,
                       "weight":float,
                       "image_url":str}
        is_broken_body = verify_request_body(request_body,field_types)
        if is_broken_body is not None:
            return is_broken_body
        
        cols = [sql.Identifier(i) for i in request_body.keys() if i not in ['manufacturer','category']]
        values = [sql.Literal(j) for i,j in request_body.items() if i not in ['manufacturer','category']]
        cols_values = [item for sublist in zip(cols,values) for item in sublist]
        placeholders = ','.join(['{}={}'] * len(cols))
        query  = sql.SQL('''DO $$
                    DECLARE
                        cat_id INTEGER;
                        manu_id INTEGER;
                        cat VARCHAR(50) := {};
                        manu VARCHAR(50) := {};
                    BEGIN
                        SELECT id INTO cat_id
                        FROM category
                        WHERE name = cat;
                         
                        IF cat_id IS NULL THEN
                            RAISE EXCEPTION 'Invalid category: %%.', cat;
                        END IF;
                        
                        SELECT id INTO manu_id
                        FROM manufacturer
                        WHERE name = manu;
                         
                        IF manu_id IS NULL THEN
                            RAISE EXCEPTION 'Invalid manufacturer: %%.', manu;
                        END IF; 
                         
                        UPDATE item SET "category_id"=cat_id,"manufacturer_id"=manu_id,%s WHERE id={};
                        IF not found then RAISE EXCEPTION 'Item not found';
                        END IF;
                    END $$;''' % placeholders).format(sql.Literal(request_body['category']),
                                       sql.Literal(request_body['manufacturer']),
                                       *cols_values,
                                       sql.SQL(str(id)))
        cur.execute(query)
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': "Item updated successfully :).",
                    'data': request_body}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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

        if item_id.isnumeric():
            request_body = {'item_id':int(item_id)}
            field_types = {'item_id':int}
            is_broken_body = verify_request_body(request_body,field_types)
            if is_broken_body is not None:
                return is_broken_body
        else:
            return {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data type you provided.'}
        
        query = '''DO $$
                   BEGIN
                    DELETE from cart_item WHERE cart_client_id=\'client123\' AND item_id=%s;
                    IF not found then RAISE EXCEPTION 'The item you are trying to delete does not exist :(.';
                    END IF;
                   END $$;'''
        cur.execute(query, (item_id,))
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': "Item removed from the shopping cart :|.",
                    'data': None}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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
        
        query = sql.SQL('''DO $$
                   DECLARE itemId INTEGER := {};
                           thisQuantity INTEGER := {};
                           thisClient VARCHAR(50) := 'client123';
                   BEGIN
                       CALL check_stock(itemId, thisQuantity);
                       CALL add_or_append_to_cart(itemId, thisQuantity, thisClient);
                   END $$;''').format(sql.Literal(str(request_body['item_id'])),
                                      sql.Literal(str(request_body['quantity'])))
        cur.execute(query)
        conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': f'Item added to the shopping cart :).',
                    'data': None}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Don\'t worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.ForeignKeyViolation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The item_id you provided doesn\'t exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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
        response = {'status': StatusCodes['success'],
                    'message': "Items retrieved successfully :).",
                    'data': data}
        return flask.jsonify(response)
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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

        if id.isnumeric():
            request_body = {'item_id':int(id)}
            field_types = {'item_id':int}
            is_broken_body = verify_request_body(request_body,field_types)
            if is_broken_body is not None:
                return is_broken_body
        else:
            return {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data type you provided.'}
        
        query = '''DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM item WHERE id = %s) THEN
                            RAISE EXCEPTION 'Item with ID = %% not found', %s;
                        END IF;
                    END $$;
                    SELECT item.id,
                            item.name,
                            category.name as category,
                            item.price,
                            item.stock,
                            item.description,
                            manufacturer.name as manufacturer,
                            item.weight,
                            item.image_url
                    FROM item
                    JOIN category ON item.category_id = category.id
                    JOIN manufacturer ON item.manufacturer_id = manufacturer.id
                    WHERE item.id = %s;'''
        cur.execute(query,(id,id,id))
        conn.commit()
        values = cur.fetchall()[0]
        cols = [desc[0] for desc in cur.description]
        data = {i:j for i,j in zip(cols,values)}
        response = {'status': StatusCodes['success'],
                    'message': "Item details retrieved successfully :).",
                    'data': data}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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
        else:
            query = sql.SQL(request_body['param'])
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
            
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except IndexError as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The parameter your providing doesnt exist :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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
                        ROW_NUMBER() OVER(PARTITION BY category_id) AS item_rank
                    FROM grouped_data
                    LEFT JOIN category ON grouped_data.category_id = category.id
                )
                SELECT ranked_grouped_data.item_name, ranked_grouped_data.name as category_name, ranked_grouped_data.total_sales
                FROM ranked_grouped_data
                WHERE item_rank <= 3
                ORDER BY total_sales DESC;'''
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
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
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

        quantities = []
        itemIds = []
        for r_b in request_body['cart']:
            is_broken_body = verify_request_body(r_b,field_cart_types,required_fields=required_cart_fields)
            if is_broken_body is not None:
                return is_broken_body
            quantities.append(sql.Literal(str(r_b['quantity']))) 
            itemIds.append(sql.Literal(str(r_b['item_id'])))
        quantities = sql.SQL(',').join(quantities)
        itemIds = sql.SQL(',').join(itemIds)

        if request_body['purchase_type'] == 'aggregate':
            query = sql.SQL(''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION aggregate()
                        RETURNS purchase_info AS $$
                        DECLARE itemIds INTEGER[];
                                quantities INTEGER[];
                                cart_quantity INTEGER;
                                purchase_price FLOAT;
                                most_recent_purchase_id INTEGER;
                                return_values purchase_info;
                                thisClient VARCHAR(50) := {};
                        BEGIN
                            -- aggregate our json cart info to our cart_item
                            itemIds := ARRAY[{}];
                            quantities := ARRAY[{}];
                            FOR i IN 1..array_length(itemIds, 1) LOOP
                                CALL check_stock(itemIds[i], quantities[i]);
                                CALL add_or_append_to_cart(itemIds[i],quantities[i],thisClient);
                                CALL get_cart_item_quantity(itemIds[i],thisClient,cart_quantity);
                                CALL update_item_stock(itemIds[i], cart_quantity);
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
                        SELECT aggregate();''').format(sql.Literal(request_body['client_id']),
                                                       itemIds,
                                                       quantities)
        elif request_body['purchase_type'] == 'mixed':    
            query = sql.SQL(''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION mixed()
                        RETURNS purchase_info AS $$
                        DECLARE itemIds INTEGER[] := ARRAY[{}];
                                quantities INTEGER[] := ARRAY[{}];
                                prices NUMERIC[];
                                purchase_price FLOAT;
                                cart_quantity INTEGER;
                                thisClient VARCHAR(50) := {};
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
                                CALL check_stock(itemIds[i], quantities[i]);
                                CALL update_item_stock(itemIds[i], quantities[i]);
                                CALL get_cart_item_quantity(itemIds[i],thisClient,cart_quantity);

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
                        SELECT mixed();''').format(itemIds,
                                                   quantities,
                                                   sql.Literal(request_body['client_id']))
                                                       
        elif request_body['purchase_type'] == 'individual':
            query = sql.SQL(''' DROP TYPE IF EXISTS purchase_info CASCADE;
                        CREATE TYPE purchase_info AS (most_recent_purchase_id INTEGER, purchase_price FLOAT);
                        CREATE OR REPLACE FUNCTION individual()
                        RETURNS purchase_info AS $$
                        DECLARE itemIds INTEGER[] := ARRAY[{}];
                                quantities INTEGER[] := ARRAY[{}];
                                purchase_price FLOAT;
                                thisClient VARCHAR(50) := {};
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
                                CALL check_stock(itemIds[i], quantities[i]);
                                CALL update_item_stock(itemIds[i], quantities[i]);
                                INSERT INTO purchase_item (quantity, item_id, purchase_id)
                                VALUES (quantities[i], itemIds[i], most_recent_purchase_id);
                            END LOOP;

                            return_values.most_recent_purchase_id := most_recent_purchase_id;
                            return_values.purchase_price := purchase_price;
                            RETURN return_values;
                        END $$ LANGUAGE plpgsql;
                        SELECT individual();''').format(itemIds,
                                                   quantities,
                                                   sql.Literal(request_body['client_id']))
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
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.ForeignKeyViolation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'From the items you provided one of the following dont exist: item_id or client_id :(.'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


# 10. get_filtered_clients (GET)
@app.route('/proj/api/clients', methods=['GET'])
def get_filtered_clients():
    try:
        conn = db_connection()
        cur = conn.cursor()

        request_body = flask.request.get_json()
        field_types = {"last_purchase_date":str,
                       "item_bought":str}
        is_broken_body = verify_request_body(request_body,field_types)
        if is_broken_body is not None:
            return is_broken_body

        if 'item_bought' in request_body:
            item_bought = sql.Literal(request_body['item_bought'])
            item_aux_query = sql.SQL('ANY(agregated_items.last_items_bought)')
        else:
            item_bought = sql.Literal('1')
            item_aux_query = sql.Literal('1')

        if 'last_purchase_date' in request_body:
            try:
                datetime.date.fromisoformat(request_body['last_purchase_date'])
            except ValueError:
                return  {'status': StatusCodes['bad_request_error'], 'Error': "Incorrect data format, should be YYYY-MM-DD"}
            last_purchase_date = sql.Literal(request_body['last_purchase_date'])
            date_aux_query = sql.SQL('DATE(last_purchase_clients.last_purchase_date)')
        else:
            last_purchase_date = sql.Literal('1')
            date_aux_query = sql.Literal('1')

        query = sql.SQL(''' WITH last_purchase_clients AS (
                                                            SELECT DISTINCT ON (purchase.client_id)
                                                                                purchase.id,
                                                                                client.id as client_id, 
                                                                                client.name, 
                                                                                client.email, 
                                                                                purchase.purchase_date as last_purchase_date
                                                            FROM purchase
                                                            FULL JOIN client ON client.id = purchase.client_id
                                                            ORDER BY purchase.client_id, purchase.purchase_date DESC
                                                            ),
                                agregated_items AS (
                                                        SELECT purchase_item.purchase_id, ARRAY_AGG(item.name) as last_items_bought
                                                        FROM purchase_item
                                                        JOIN item ON item.id = purchase_item.item_id
                                                        GROUP BY purchase_item.purchase_id
                                                    )

                            SELECT last_purchase_clients.client_id, 
                                    last_purchase_clients.name, 
                                    last_purchase_clients.email,
                                    last_purchase_clients.last_purchase_date,
                                    agregated_items.last_items_bought
                            FROM last_purchase_clients
                            LEFT JOIN agregated_items ON agregated_items.purchase_id = last_purchase_clients.id
                            WHERE {} = {}
                            AND   {} = {};''').format(item_bought,
                                                      item_aux_query,
                                                      date_aux_query,
                                                      last_purchase_date)
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = []
        cols = [desc[0] for desc in cur.description]
        for row in values:
            formated_row = {i:j for i,j in zip(cols,row)}
            data.append(formated_row)
        response = {'status': StatusCodes['success'],
                    'message': "Clients retrieved successfully :).",
                    'data': data}

    except UnsupportedMediaType as error:
        query = ''' WITH last_purchase_clients AS (
                                                    SELECT DISTINCT ON (purchase.client_id)
                                                                        purchase.id,
                                                                        client.id as client_id, 
                                                                        client.name, 
                                                                        client.email, 
                                                                        purchase.purchase_date as last_purchase_date
                                                    FROM purchase
                                                    FULL JOIN client ON client.id = purchase.client_id
                                                    ORDER BY purchase.client_id, purchase.purchase_date DESC
                                                    ),
                        agregated_items AS (
                                                SELECT purchase_item.purchase_id, ARRAY_AGG(item.name) as last_items_bought
                                                FROM purchase_item
                                                JOIN item ON item.id = purchase_item.item_id
                                                GROUP BY purchase_item.purchase_id
                                            )

                    SELECT last_purchase_clients.client_id, 
                            last_purchase_clients.name, 
                            last_purchase_clients.email,
                            last_purchase_clients.last_purchase_date,
                            agregated_items.last_items_bought
                    FROM last_purchase_clients
                    LEFT JOIN agregated_items ON agregated_items.purchase_id = last_purchase_clients.id;'''
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = []
        cols = [desc[0] for desc in cur.description]
        for row in values:
            formated_row = {i:j for i,j in zip(cols,row)}
            data.append(formated_row)
        response = {'status': StatusCodes['success'],
                    'message': "Clients retrieved successfully :).",
                    'data': data}
        return flask.jsonify(response)        
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


# 11. Add Client (POST)
@app.route('/proj/api/clients', methods=['POST'])
def add_client():
    try:
        conn = db_connection()
        cur = conn.cursor()

        request_body = flask.request.get_json()
        required_fields = ["id","name"]
        field_types = {"id":str,
                       "email":str,
                       "name":str}
        is_broken_body = verify_request_body(request_body,field_types,required_fields=required_fields)
        if is_broken_body is not None:
            return is_broken_body
        
        if 'email' in request_body:
            email = sql.Literal(request_body['email'])
            query = sql.SQL(''' INSERT INTO client (id,name,email) 
                                        VALUES ({},{},{});''').format(sql.Literal(str(request_body['id'])),
                                                                    sql.Literal(str(request_body['name'])),
                                                                    email)
            cur.execute(query)
            conn.commit()     
        else:
            email = None
            query = sql.SQL(''' INSERT INTO client (id,name,email) 
                                        VALUES ({},{},%s);''').format(sql.Literal(str(request_body['id'])),
                                                                    sql.Literal(str(request_body['name'])))
            cur.execute(query,[email])
            conn.commit()
        response = {'status': StatusCodes['success'],
                    'message': 'Client added successfully :).',
                    'data': request_body}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.UniqueViolation as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'The id you provided already exists :(.'}
        conn.rollback()
    except BadRequest as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be an error with the JSON format you are providing, make sure its a valid JSON.'}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


# 12. Get Client Orders (GET) 
@app.route('/proj/api/clients/<client_id>/orders', methods=['GET'])
def get_client_order(client_id):
    try:
        conn = db_connection()
        cur = conn.cursor()

        if client_id.isnumeric():
            request_body = {'client_id':int(client_id)}
            field_types = {'client_id':int}
            is_broken_body = verify_request_body(request_body,field_types)
            if is_broken_body is not None:
                return is_broken_body
        else:
            return {'status': StatusCodes['bad_request_error'], 'Error': 'There seems to be a problem with the data type you provided.'}

        query = sql.SQL('''DO $$
                            DECLARE clientId VARCHAR(50) = {client};
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT 1 FROM client WHERE id = clientId
                                ) THEN
                                    RAISE EXCEPTION 'Client ID not found: %', clientId;
                                END IF;
                            END $$;

                            WITH aggregated_items AS (
                                SELECT purchase_id, JSONB_AGG(jsonb_build_object('item_id', item_id, 'quantity', quantity)) AS items_info
                                FROM purchase_item
                                GROUP BY purchase_id
                            )
                            SELECT purchase.id as order_id,
                                aggregated_items.items_info AS items,
                                purchase.price AS total_price, 
                                purchase.purchase_date AS order_date
                            FROM purchase
                            JOIN aggregated_items ON aggregated_items.purchase_id = purchase.id
                            WHERE purchase.client_id = {client};''').format(client=sql.Literal(str(client_id)))
        cur.execute(query)
        conn.commit()
        values = cur.fetchall()
        data = []
        cols = [desc[0] for desc in cur.description]
        for row in values:
            formated_row = {i:j for i,j in zip(cols,row)}
            data.append(formated_row)
        response = {'status': StatusCodes['success'],
                    'message': "Client orders retrieved successfully :).",
                    'data': data}
    except psycopg2.OperationalError as error:
        response = {'status': StatusCodes['api_error'], 'Error': 'Ups, this service is currently down! Dont worry, we are already working on it!'}
        conn.rollback()
        return flask.jsonify(response)
    except psycopg2.errors.RaiseException as error:
        response = {'status': StatusCodes['bad_request_error'], 'Error': str(error).split('\n')[0]}
        conn.rollback()
        return flask.jsonify(response)
    except Exception as error:
        response = {'Error': f'An error ocurred - {type(error).__name__}'}
        conn.rollback()
        return flask.jsonify(response)
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)



if __name__ == '__main__':
    # # Create the tables in the db
    # create_tables()

    # # Load data into the tables in the db
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
    # purchase['price'] = purchase['price']*purchase['purchase_quantity']
    # purchase = purchase[['purchase_date','price','client_id']]
    # purchase_item = df.sort_values(by=['purchase_date'])[~df['purchase_date'].isnull()].loc[:,['purchase_quantity','item_id']]
    # purchase_item['id_purchase'] = [1,2,3,4]
    # purchase_item = purchase_item[['purchase_quantity','id_purchase','item_id']].rename(columns={"purchase_quantity":"quantity","id_purchase": "purchase_id"})

    # table_dfs = [category,manufacturer,item,client,cart,purchase,purchase_item]
    # table_names = ['category','manufacturer','item','client','cart','purchase','purchase_item']
    # for df,name in zip(table_dfs,table_names):
    #     insert_df_in_db(df, name)

    # run the app
    app.run(host='127.0.0.1', debug=True, threaded=True, port=8080)

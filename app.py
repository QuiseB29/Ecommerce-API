from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
import password

app = Flask(__name__)
ma = Marshmallow(app)
#Schemas that hold your information
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone", "id")
        
class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    
    class Meta:
        fields = ("username", "password","id")

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.String(required=True)
    
    class Meta:
        fields = ("name", "price", "id")
class OrderSchema(ma.Schema):
    orders = fields.String(required=True)
    track = fields.String(required=True)
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_account_schema = CustomerAccountSchema()
customers_account_schema = CustomerAccountSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

def get_db_connection():
    
    db_name = "e_commerce_db"
    user = "root"
    password = "Auston123!"
    host = "127.0.0.1"
    #establish database connection to SQL
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        
        print("Connected to MYSQL database successfully")
        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None
    
    #Routes to PostMan
@app.route('/')
def home():
    return "Welcome Ecommerce Customers"
#Retrieve Customers/CustomerAccount/Products
@app.route("/customers", methods=["GET"])
def get_customers():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM customers"
        
        cursor.execute(query)
        
        customers = cursor.fetchall()
        
        return customers_schema.jsonify(customers)
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal server Error"})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/customeraccount", methods=["GET"])
def get_customer_account():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM customeraccount"
        
        cursor.execute(query)
        
        customers_account = cursor.fetchall()
        
        return customers_account_schema.jsonify(customers_account)
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal server Error"})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/products", methods=["GET"])
def get_products():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM products"
        
        cursor.execute(query)
        
        products = cursor.fetchall()
        
        return products_schema.jsonify(products)
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal server Error"})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM orders"
        
        cursor.execute(query)
        
        orders = cursor.fetchall()
        
        return orders_schema.jsonify(orders)
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal server Error"})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
  #add customers/customer accounts/products          
@app.route("/customers", methods=["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone'])
        
        query = "INSERT INTO customers (name,email,phone) VALUES (%s, %s, %s)"
        
        cursor.execute(query, new_customer)
        conn.commit()
        
        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route("/customeraccount", methods=["POST"])
def add_customer_account():
    try:
        customer_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        new_customer_account = (customer_data['username'], customer_data['password'])
        
        query = "INSERT INTO customeraccount (username, password) VALUES (%s, %s)"
        
        cursor.execute(query, new_customer_account)
        conn.commit()
        
        return jsonify({"message": "New customer account added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route("/products", methods=["POST"])
def add_products():
    try:
        customer_data = product_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        new_product = (customer_data['name'], customer_data['price'])
        
        query = "INSERT INTO products (name,price) VALUES (%s, %s)"
        
        cursor.execute(query, new_product)
        conn.commit()
        
        return jsonify({"message": "New product added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
#update customers, customer accounts, products
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        updated_customer = (customer_data['name'], customer_data['email'], customer_data['phone'], id)
        
        query = "UPDATE customers SET name = %s, email = %s, phone = %s WHERE id = %s"
        
        cursor.execute(query, updated_customer)
        conn.commit()
        
        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route("/customeraccount/<int:id>", methods=["PUT"])
def update_customer_account(id):
    try:
        customer_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        updated_customer_account = (customer_data['username'], customer_data['password'], id)
        
        query = "UPDATE customeraccount SET username = %s, password = %s WHERE id = %s"
        
        cursor.execute(query, updated_customer_account)
        conn.commit()
        
        return jsonify({"message": "Update customer successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        customer_data = product_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        updated_product = (customer_data['name'], customer_data['price'], id)
        
        query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        
        cursor.execute(query, updated_product)
        conn.commit()
        
        return jsonify({"message": "product update successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
#delete customer, customer account, products
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        customer_to_remove = (id,)
        
        cursor.execute("SELECT * FROM customers where Id = %s", customer_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error":"Customer not found"}), 404
        query = "DELETE FROM customers WHERE id = %s"
        cursor.execute(query,customer_to_remove)
        conn.commit()
        
        return jsonify({"message": "Customer removed successfully"}), 200
        
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/customeraccount/<int:id>", methods=["DELETE"])
def delete_customer_account(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        customer_account_to_remove = (id,)
        
        cursor.execute("SELECT * FROM customers where Id = %s", customer_account_to_remove)
        customer_account = cursor.fetchone()
        if not customer_account:
            return jsonify({"error":"Customer account not found"}), 404
        query = "DELETE FROM customeraccount WHERE id = %s"
        cursor.execute(query,customer_account_to_remove)
        conn.commit()
        
        return jsonify({"message": "Customer account removed successfully"}), 200
        
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        product_to_remove = (id,)
        
        cursor.execute("SELECT * FROM products where Id = %s", product_to_remove)
        product = cursor.fetchone()
        if not product:
            return jsonify({"error":"Customer not found"}), 404
        query = "DELETE FROM products WHERE id = %s"
        cursor.execute(query,product_to_remove)
        conn.commit()
        
        return jsonify({"message": "Product removed successfully"}), 200
        
    except Error as e:
        print(f"Error: {e}")
        
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
if __name__ == '__main__':
    app.run(debug=True)
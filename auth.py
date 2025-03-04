from db_conn import DBConnect
import hashlib
db = DBConnect()
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
def register_user(username, password, full_name, phone, email, role):
    hashed_password = hash_password(password)
    query = """INSERT INTO users (username, password, full_name, phone, email, role) VALUES (%s, %s, %s, %s, %s, %s)"""
    params = (username, hashed_password, full_name, phone, email, role)
    success = db.execute_query(query, params)
    if success:
        print("User registered successfully")
        return True
    else:
        print("User registration failed")
        return False
def login(username, password):
    hashed_password = hash_password(password)
    query = """select * from users where username = %s and password = %s"""
    params = (username, hashed_password)
    result = db.fetch_one(query, params)
    if result:
        print("Login successful")
        return result[0]
    else:
        print("Login failed")
        return None
def logout():
    print("Logged out")
    return True

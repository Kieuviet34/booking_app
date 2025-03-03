import mysql.connector
from mysql.connector import Error

class DBConnect:
    def __init__(self, host="localhost", user="root", password="Kieuviet2004@", database="qlbv"):
        self.host = host
        self.user = user
        self.password = password  
        self.database = database
        self.connection = None
        self.connect()
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(e)
            self.connection = None
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Đã ngắt kết nối cơ sở dữ liệu.")
    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()

        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params or ())
                self.connection.commit()
                cursor.close()
                return True
            except Error as e:
                print(f"Lỗi khi thực thi câu lệnh: {e}")
                return False
        return False
    def fetch_data(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()

        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                cursor.close()
                return result
            except Error as e:
                print(f"Lỗi khi lấy dữ liệu: {e}")
                return None
        return None
    def fetch_one(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()

        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params or ())
                result = cursor.fetchone()
                cursor.close()
                return result
            except Error as e:
                print(f"Lỗi khi lấy một dòng dữ liệu: {e}")
                return None
        return None

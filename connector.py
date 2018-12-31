from flask import  Flask
import mysql.connector

class connector():
    def __init__(self, host='localhost', user='root', password='', database=''):
        self.cnx = mysql.connector.connect(user=user, password=password, database=database)

    def get(self, query, data):
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, data)
            res = cursor.fetchall()
            self.cnx.commit()
            self.cnx.close()
            return res
        except Exception as error:
            return str(error)

    def set(self, query, data):
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query, data)
            self.cnx.commit()
            self.cnx.close()
            return 'success'
        except Exception as error:
            return str(error)

    def simpleGet(self, query):
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query)
            res = cursor.fetchall()
            self.cnx.commit()
            self.cnx.close()
            return res
        except Exception as error:
            return str(error)

    def simpleSet(self, query):
        try:
            cursor = self.cnx.cursor(buffered=True)
            cursor.execute(query)
            self.cnx.commit()
            self.cnx.close()
            return 'success'
        except Exception as error:
            return str(error)

##用于将excel表中的数据导入数据库中
#同时建立数据库
from flask_sqlalchemy import SQLAlchemy
from flask import  Flask
import pymysql
from datetime import datetime

import os

filename = './movie.xls'
DATABASE = './'
app = Flask(__name__)
basedir = os.path.dirname(__file__)
app.debug = True


import xlrd
import sys



def read_excel():
    workbook = xlrd.open_workbook('./movie.xls')
    sheet = workbook.sheet_names()
    sheet = workbook.sheet_by_name('movie')
    nrows = sheet.nrows
    print(nrows)
    movies = []
    for nrow in range(1,nrows):
        sub_movie = sheet.row_values(nrow-1)
        if(len(sub_movie[0])>45):
            continue
        movies.append(sheet.row_values(nrow-1))
    return movies



#数据库的电影表的数据
filename = 'movie.xls'


# '''创建数据模型'''
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wzd0606@127.0.0.1:3306/flask?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASEE_PASSWORD'] = 'wzd0606'
app.config['MYSQL_DATABASE_DB'] = 'MovieTheatre'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


db = SQLAlchemy(app)

# #创建ORDER表
# class Attend(db.Model):
#
#     # __tabelname__ = 'Order'
#     # Order_ID = db.Column(db.String(64), primary_key=True)
#     # Customer_ID = db.Column(db.String(64), unique=True, index=True)
#     # Price = db.Column(db.Integer)
#     # Schedule_ID = db.Column(db.Integer)
#     # Order_BuyDate = db.Column(db.DATE, default=datetime.now)
#     # Order_BuyTime = db.Column(db.DateTime)
#     __tabel_name__ = 'Attend'
#     Customer_idCustomer = db.Column(db.Integer,nullable=False,primary_key=True,db.ForeignKey('Customer.idCustomer',ondelete="NO ACTION"))
#
#     Showing_idShowing = db.Column(db.Integer,nullable=False,primary_key=True,db.ForeignKey('Showing.idShowing',ondelete="NO ACTION"))
#     Rating = db.Column(db.SmallInteger,nullable=True)
#
#     def __init__(self, username):
#         self.username = username
#
#     def __repr__(self):
#         return '<User %r>' %(self.username)
#
#
# ##创建用户表
# class Customer(db.Model):
#     __
#
# ##创建座位表
# class Seat(db.Model):
#     __table_name = 'Seat'
#     Order_ID = db.Column(db.String(64), primary_key=True,)
#     Seat_ID = db.Column(db.INTEGER, unique=True)
#     Hall_ID = db.Column(db.INTEGER)
#     Seat_Row = db.Column(db.INTEGER)
#     Seat_Column = db.Column(db.INTEGER)
#
#     def __init__(self,Order_ID,Seat_ID):
#         self.Order_ID = Order_ID
#         self.Seat_ID = Seat_ID
#
#
#
# ##创建排片表
# class Schedule(db.Model):
#     __tabel_name__ = 'Schedule'
#     Schedule_ID = db.Column(db.String(64),primary_key=True)
#     Movie_ID = db.Column(db.String(64),index = True)
#     Hall_ID = db.Column(db.String(64))
#     Price = db.Column(db.Integer)
#     Begin_time = db.Column(db.DateTime)
#
#
# ##创建电影表
# class Movie(db.Model):
#     __table_name__ = 'Movie'
#     Movie_ID = db.Column(db.VARCHAR(3),primary_key=True)
#     Movie_Name = db.Column(db.VARCHAR(128))
#     Movie_Score = db.Column(db.VARCHAR(3))
#     Movie_Director = db.Column(db.VARCHAR(64))
#     Movie_Actor = db.Column(db.VARCHAR(64))
#     Movie_Type = db.Column(db.VARCHAR(41))
#     Movie_Country = db.Column(db.VARCHAR(41))
#     Movie_Year = db.Column(db.VARCHAR(4))
#
#
# ##创建放映厅表
# class Hall(db.Model):
#     __table_name__ = 'Hall'
#     Hall_ID = db.Column(db.String(64),primary_key=True)
#     Hall_NUM = db.Column(db.INTEGER)
#     Hall_current = db.Column(db.INTEGER)
#
#
# class User(db.Model):
#     __table_name__ = 'User'
#     User_ID = db.Column(db.String(64),primary_key=True)
#     User_Name = db.Column(db.String(64))
#     User_Password = db.Column(db.String(64))
#     User_Email = db.Column(db.String(64))
#
#     def to_json(self):
#         return {
#             "User_ID": self.User_ID,
#             "User_Name": self.User_Name
#         }
#
#
def get_conn():
    host = '127.0.0.1'
    port = 3306
    database = 'MovieTheatre'
    user = 'root'
    password = "wzd0606"
    conn = pymysql.Connect(
        host=host,
        port=port,
        db=database,
        user=user,
        password=password,
        charset='utf8mb4')

    return conn

#
#
#
# # class User(object):
# #     def __init__(self, user_id, user_name):
# #         self.user_id = user_id
# #         self.user_name = user_name
# #
# #     def save(self):
# #         conn = get_conn()
# #         cursor = conn.cursor()
# #         sql = 'Insert into user (user_id,user_name)'
# #         cursor.execute(sql, (self.user_id,self.user_name))
# #         conn.commit()
# #         cursor.close()
# #         conn.close()
# #
# #     @staticmethod
# #
# #
# #     def query_all():
# #         conn = get_conn()
# #         cursor = conn.cursor()
# #
# #         sql = 'select * from user '
# #
# #         cursor.execute(sql)
# #         rows = cursor.fetchall()
# #         user = []
# #
# #         for row in rows:
# #             user = User(row[0],row[1])
# #
# #             user.append(user)
# #
# #         conn.commit()
# #         cursor.close()
# #         conn.close()
# #         return user
# #
# #     def __str__(self):
# #         return "id:{} name{}".format(self.user_id,self.user_name)
# #
# #
if __name__ == '__main__':

    db.drop_all()
    db.create_all()
    conn = get_conn()
    cursor = conn.cursor()
    movie_name = read_excel()
    sql1 = "insert into Movie" \
          "(" \
          "idMovie," \
          "MovieName," \
          "Movie_Score ," \
          "Movie_Director," \
          "Movie_Actor ," \
          "Movie_Type ," \
          "Movie_Country ," \
          "MovieYear " \
          ") values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s)"

    ##种类初始化
    sql2 = "insert into Genre" \
           "(" \
           "Genre," \
           "Movie_idMovie" \
           ")values " \
           "(%s,%s)"

    #插入时间
    sql3 = "insert into Showing " \
           "values (%s,%s,%s,%s,%s)"
    conn.commit()

    showing = [(1,'2018-02-11 21:30:00',1,1,5),
               (2,'2018-02-11 19:30:00',1,2,5),
               (3,'2018-02-11 19:00:00',2,3,2),
               (4,'2018-03-12 19:00:00',3,1,8),
               (5,'2018-03-12 21:00:00',4,1,8),
               (6,'2018-03-13 19:00:00',4,2,8),
               (7,'2018-03-20 19:00:00',4,1,4),
               (8,'2018-03-20 21:00:00',5,1,6),
               (9,'2018-03-22 20:30:00',8,2,4),
               (10,'2018-03-22 21:00:00',9,3,6),
               (11,'2018-03-20 19:00:00',10,2,8),
               (12,'2018-03-21 19:00:00',11,1,5),
               (13,'2018-03-23 22:00:00',11,1,3),
               (14,'2018-02-11 21:00:00',12,2,1)
               ]
    print(showing[1][1])
    # datetime.strptime(showing[1][1],"%Y-%m-%d %H:%M:%S")
    for i in showing:
        datetime.strptime(i[1], "%Y-%m-%d %H:%M:%S")

    print(showing[1])
    print(movie_name[1][6])
    for i in range(1,20):
        cursor.execute(sql1, (str(i),
                             movie_name[i][0],
                             float(movie_name[i][1]),
                             movie_name[i][2],
                             movie_name[i][3],
                             movie_name[i][4],
                             movie_name[i][5],
                             movie_name[i][6]))

        cursor.execute(sql2,(movie_name[i][4],
                             str(i)))
    cursor.executemany(sql3, showing)
    conn.commit()

    cursor.close()
    conn.close()



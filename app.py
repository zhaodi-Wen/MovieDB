# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, render_template_string, g
import mysql.connector

app = Flask(__name__)
user = 'User'


@app.route("/")
@app.route("/login")
def main():
    global user
    user = 'User'
    return render_template('login.html', tag=user)

@app.route('/register')
def registerPage():
    global user
    return render_template('register.html', tag=user)


@app.route('/login', methods=["POST"])
def login():
    global user
    email = request.form['email']
    name = request.form['user_name']
    query = (
        "SELECT FirstName, LastName FROM Customer WHERE EmailAddress = %s"
    )
    data = (email,)
    # change the return stuff to list
    user_info = list(sum(sqlGetter1(query,data), ()))
    print(user_info)
    print(len(user_info))
    if len(user_info) == 0:
        error = 'Name and Email does not match.'
        return render_template('login.html', error=error, tag=user)
    else:
        fullname = user_info[0] +' '+ user_info[1]
        if name != fullname:
            error = 'Name and Email does not match.'
            return render_template('login.html', error=error, tag=user)
        else:
            user = fullname
            return redirect(url_for('userPage', username=user))


@app.route('/register', methods=["POST"])
def register():
    global user
    fName = request.form['first_name']
    lName = request.form['last_name']
    email = request.form['email']
    gender = request.form['gender']
    query = (
        "insert ignore into Customer values(0, %s, %s, %s, %s);"
    )
    data = (fName, lName, email, gender)
    sqlSetter1(query, data)
    user = fName + ' ' + lName
    return redirect(url_for('userPage', username=user))


###################################################

@app.route("/movie")
def moviePage():
    global user
    query = ("SELECT * FROM Movie")
    movies = sqlGetter(query)
    return render_template('movie.html', movies=movies, tag=user)


@app.route('/movie/<movieKey>', methods=["POST"])
def movieSortBy(movieKey):
    print(movieKey)
    print(request.data)
    global user
    query = ("SELECT * FROM Movie ORDER BY " + movieKey + "; ")
    movies = sqlGetter(query)
    return render_template('movie.html', movies=movies, tag=user)


@app.route('/movie/addMovie', methods=["POST"])
def movieAdd():
    mName = request.form['movieName']
    mYear = request.form['relaseYear']
    query = (
        "INSERT IGNORE INTO Movie VALUES (0,'" + mName + "'," + mYear + ");"
    )
    sqlSetter(query)
    return redirect(url_for('moviePage'))


@app.route('/movie/removeMovie', methods=["POST"])
def movieRemove():
    mName = request.form['movieName']
    mID = request.form['movieID']
    query = (
        "DELETE FROM Movie WHERE idMovie=" + mID + " AND MovieName='" + mName + "';"
    )
    sqlSetter(query)
    return redirect(url_for('moviePage', username=mName))


@app.route('/movie/editMovie', methods=["POST"])
def movieEdit():
    mName = request.form['movieName']
    mID = request.form['movieID']
    mYear = request.form['relaseYear']
    query = (
        "UPDATE Movie SET MovieYear=%s, MovieName=%s WHERE idMovie=%s"
    )
    data = (mYear, mName, mID)
    sqlSetter(query)
    return redirect(url_for('moviePage',username=mName))

###################################################

@app.route("/showing")
def showingPage():
    global user
    query = ("SELECT * FROM Showing s LEFT OUTER JOIN Movie m ON s.Movie_idMovie = m.idMovie;")
    showings = sqlGetter(query)
    query = ("SELECT DISTINCT Movie_Type FROM Movie")
    genres = sqlGetter(query)
    genres = [genre[0].split('/')[0] for genre in genres]
    print(genres)
    genres = list(set(genres))
    print(genres)
    query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
    dates = sqlGetter(query)
    query = ("SELECT idCustomer, FirstName, LastName FROM Customer WHERE NOT (FirstName='Super' AND LastName='User') ")
    customers = sqlGetter(query)
    return render_template('showing.html', showings=showings, tag=user, genres=genres, customers=customers, dates=dates)


@app.route("/showing/<showingKey>", methods=["POST"])
def showingSortBy(showingKey):
    global user
    query = ("SELECT * FROM Showing s LEFT OUTER JOIN Movie m ON s.Movie_idMovie = m.idMovie ORDER BY " + showingKey + ";")
    showings = sqlGetter(query)
    query = ("SELECT DISTINCT Genre FROM Genre")
    genres = sqlGetter(query)
    genres = [genre[0].split('/')[0] for genre in genres ]
    print(genres)
    query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
    dates = sqlGetter(query)
    return render_template('showing.html', showings=showings, tag=user, genres=genres, dates=dates)

@app.route('/showing/search', methods=["POST"])
def showingSearch():
    global user
    query = ("SELECT DISTINCT Genre FROM Genre")
    genres = sqlGetter(query)
    genres = [genre[0].split('/') for genre in genres]
    genres = list(set([j for i in genres for j in i]))
    print(genres)

    query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
    dates = sqlGetter(query)
    query =(
        "Drop view  if EXISTS temp "
    )
    sqlSetter(query)
    query = (
        "create view temp as select Showing_idShowing 'showID', count(Customer_idCustomer) 'countAttend' "
        "from Attend a right outer join Showing s on a.Showing_idShowing=s.idShowing "
        "group by Showing_idShowing;"
    )
    sqlSetter(query)
    checked = 'check' in request.form
    if checked == True:
        if request.form['movieName']:
            query = (
                "SELECT * FROM Showing "
                "LEFT OUTER JOIN Movie "
                "ON Movie_idMovie = idMovie "
                "LEFT OUTER JOIN Genre "
                "ON idMovie = Genre.Movie_idMovie "
                "WHERE Genre like %s "
                "AND ShowingDateTime > %s "
                "AND ShowingDateTime < %s "
                "AND MovieName like %s "
                "AND idShowing NOT IN "
                "(select idShowing from temp t "
                "left outer join Showing s "
                "on t.showID=s.idShowing "
                "left outer join TheatreRoom th "
                "on s.TheatreRoom_RoomNumber=th. RoomNumber "
                "where Capacity<=countAttend)"
            )
        else:
            query = (
                "SELECT * FROM Showing "
                "LEFT OUTER JOIN Movie "
                "ON Movie_idMovie = idMovie "
                "LEFT OUTER JOIN Genre "
                "ON idMovie = Genre.Movie_idMovie "
                "WHERE Genre like %s "
                "AND ShowingDateTime > %s "
                "AND ShowingDateTime < %s "
                "AND idShowing NOT IN "
                "(select idShowing from temp t "
                "left outer join Showing s "
                "on t.showID=s.idShowing "
                "left outer join TheatreRoom th "
                "on s.TheatreRoom_RoomNumber=th. RoomNumber "
                "where Capacity<=countAttend)"
            )

    else:
        if request.form['movieName']:
            query = (
                "SELECT * FROM Showing "
                "LEFT OUTER JOIN Movie "
                "ON Movie_idMovie = idMovie "
                "LEFT OUTER JOIN Genre "
                "ON idMovie = Genre.Movie_idMovie "
                "WHERE Genre like %s"
                "AND ShowingDateTime > %s "
                "AND ShowingDateTime < %s "
                "AND MovieName like %s"
            )
        else:
            query = (
                "SELECT * FROM Showing "
                "LEFT OUTER JOIN Movie "
                "ON Movie_idMovie = idMovie "
                "LEFT OUTER JOIN Genre "
                "ON idMovie = Genre.Movie_idMovie "
                "WHERE Genre like %s "
                "AND ShowingDateTime > %s "
                "AND ShowingDateTime < %s "
            )
    print(query)
    if request.form['movieName']:
        data = ('%'+request.form['genre']+'%', request.form['startDate'], request.form['endDate'], '%' + request.form['movieName'] + '%')
    else:
        data = ('%'+request.form['genre']+'%', request.form['startDate'], request.form['endDate'])

    print(data)
    showings = sqlGetter1(query, data)
    print('showings',showings)
    query = ("drop view temp")
    sqlSetter(query)
    return render_template('showing.html', showings=showings, tag=user, genres=genres, dates=dates)



@app.route('/showing/addShow', methods=["POST"])
def showingAdd():
    mName = request.form['movieName']
    sTime = request.form['showingTime']
    sRoom = request.form['showingRoom']
    sPrice = request.form['showingPrice']
    query = ("SELECT idMovie FROM Movie WHERE MovieName='" + mName + "';")
    mID = str(list(sum(sqlGetter(query), ()))[0])
    print(mID)
    print(type(mID))
    query = ("INSERT IGNORE INTO Showing VALUES (0, '" + sTime +
             "', " + mID + ", " + sRoom + ", " + sPrice + ");")
    print(query)
    sqlSetter(query)
    return redirect(url_for('showingPage'))


@app.route('/showing/removeShow', methods=["POST"])
def showingRemove():
    mName = request.form['movieName']
    sID = request.form['showingID']
    query = ("SELECT idMovie FROM Movie WHERE MovieName='" + mName + "';")
    mID = str(list(sum(sqlGetter(query), ()))[0])
    query = (
        "DELETE FROM Showing WHERE Movie_idMovie=" + mID + " AND idShowing=" + sID + ";"
    )
    sqlSetter(query)
    return redirect(url_for('showingPage'))


@app.route('/showing/editShow', methods=["POST"])
def showingShow():
    mName = request.form['movieName']
    query = ("SELECT idMovie FROM Movie WHERE MovieName='" + mName + "';")
    mID = sqlGetter(query)
    if (len(mID) == 0):
        return redirect(url_for('showingPage'))
    else:
        mID = str(list(sum(mID, ()))[0])
        print(mID)
        print(type(mID))
        query = (
            "UPDATE Showing SET ShowingDateTime=%s, Movie_idMovie=%s, TheatreRoom_RoomNumber=%s, TicketPrice=%s WHERE idShowing=%s"
        )
        data = (request.form['showingTime'], mID, request.form['showingRoom'], request.form['showingPrice'], request.form['showingID'])
        sqlSetter1(query, data)
        return redirect(url_for('showingPage'))

#need to have a visual queue for the user that purchase was successful
@app.route('/showing/purchaseTicket', methods=["POST"])
def purchaseTicket():
    print("in ticker")
    print(request.form)
    checked = 'check' in request.form
    print(request.form)
    # try:
    # price = request.form["purchasePrice"]
    # print(price)
    showing = request.form["showingToPurchase"]
    customer = request.form["purchaseCustomer"]
    print(showing)
    data = (customer,showing)
    print("hello")
    print('data',data)
    query = ("INSERT  INTO Attend  VALUES (%s, %s, NULL);")
    sqlSetter1(query, data)
    return redirect(url_for("showingPage"))
    # except Exception as error:
    #     print("ERROR")
    #     return str(error)

###################################################

@app.route('/<username>')
def userPage(username):
    global user
    nList = user.split(' ')
    print(nList)
    data = (nList[0], nList[1])
    query = (
        "SELECT * FROM Customer WHERE FirstName=%s AND LastName=%s"
    )
    profile = sqlGetter1(query, data)
    print(profile)
    query = (
        "SELECT * FROM Customer WHERE NOT (FirstName='Super' AND LastName='User')"
    )
    customers = sqlGetter(query)
    query = (
        "select s.idShowing, m.MovieName, s.ShowingDateTime, a.Rating from "
        "Customer c left outer join Attend a on c.idCustomer = a.Customer_idCustomer "
        "left outer join Showing s on a.Showing_idShowing=s.idShowing "
        "left outer join Movie m on s.Movie_idMovie=m.idMovie "
        "where FirstName=%s and LastName=%s"
    )
    history = sqlGetter1(query, data)
    return render_template('user.html', fullname=user, tag=user, profile=profile, customers=customers, history=history)

@app.route('/user/<userKey>', methods=["POST"])
def userSortById(userKey):
    global user
    nList = user.split(' ')
    data = (nList[0], nList[1])
    query = (
        "SELECT * FROM Customer WHERE FirstName=%s AND LastName=%s"
    )
    profile = sqlGetter1(query, data)
    query = (
        "select s.idShowing, m.MovieName, s.ShowingDateTime, a.Rating from "
        "Customer c left outer join Attend a on c.idCustomer = a.Customer_idCustomer "
        "left outer join Showing s on a.Showing_idShowing=s.idShowing "
        "left outer join Movie m on s.Movie_idMovie=m.idMovie "
        "where FirstName=%s and LastName=%s "
        "ORDER BY " + userKey
    )
    history = sqlGetter1(query, data)
    return render_template('user.html', fullname=user, tag=user, profile=profile, history=history)

#need to let the user know it was successful
@app.route('/<username>/addRating', methods=["POST"])
def addRating(username):
    try:
        global user
        userData = request.form.get("customerId", 'default value')
        usernameQuery = ("SELECT idCustomer FROM Customer WHERE FirstName=%s AND LastName=%s")
        data = (userData.split(" ")[0], userData.split(" ")[1])
        userId = sqlGetter1(usernameQuery, data)[0][0]
        data = (request.form["rating"], str(userId), request.form["showingToRate"])
        query = ("UPDATE Attend SET Rating=%s where Customer_idCustomer=%s AND Showing_idShowing=%s")
        sqlSetter1(query, data)
        return redirect(url_for('userPage', username=user))
    except Exception as error:
        return str(error)


###################################################
#admin user

@app.route('/admin/addUser', methods=["POST"])
def adminAddUser():
    try:
        global user
        data = (request.form["customer_id"], request.form["first_name"], request.form["last_name"], request.form["email"], request.form["gender"])
        query = ("INSERT INTO Customer (idCustomer, FirstName, LastName, EmailAddress, Sex) VALUES (%s, %s, %s, %s, %s)")
        sqlSetter1(query, data)
        return redirect(url_for('userPage', username='Super User'))
    except Exception as error:
        return str(error)


@app.route('/admin/removeUser', methods=["POST"])
def adminRemoveUser():
    try:
        global user
        data = (request.form["customer_id"])
        query = ("DELETE FROM Customer where idCustomer=%s")
        sqlSetter1(query, (data,))
        return redirect(url_for('userPage', username='Super User'))
    except Exception as error:
        return str(error)


@app.route('/admin/editUser', methods=["POST"])
def adminEditUser():
    try:
        global user
        data = (request.form["first_name"], request.form["last_name"], request.form["email"], request.form["gender"], request.form["userId"])
        query = ("UPDATE Customer SET FirstName=%s, LastName=%s, EmailAddress=%s, Sex=%s WHERE idCustomer = %s")
        sqlSetter1(query, data)
        return redirect(url_for('userPage', username='Super User'))
    except Exception as error:
        return str(error)


@app.route('/admin/<adminKey>', methods=["POST"])
def adminPage(adminKey):
    global user
    nList = user.split(' ')
    data = (nList[0], nList[1])
    query = (
        "SELECT * FROM Customer WHERE FirstName=%s AND LastName=%s"
    )
    profile = sqlGetter1(query, data)
    query = (
        "SELECT * FROM Customer WHERE NOT (FirstName='Super' AND LastName='User')"
        "order by " + adminKey
    )
    customers = sqlGetter(query)
    query = (
        "select s.idShowing, m.MovieName, s.ShowingDateTime, a.Rating from "
        "Customer c left outer join Attend a on c.idCustomer = a.Customer_idCustomer "
        "left outer join Showing s on a.Showing_idShowing=s.idShowing "
        "left outer join Movie m on s.Movie_idMovie=m.idMovie "
        "where FirstName=%s and LastName=%s "
    )
    history = sqlGetter1(query, data)
    return render_template('user.html', fullname=user, tag=user, profile=profile, customers=customers, history=history)


###################################################
@app.route('/genre')
def genrePage():
    global user
    query = ("select Genre, idMovie, MovieName from Genre g right outer join Movie m on g.Movie_idMovie=m.idMovie;")
    genres = sqlGetter(query)
    # genres = [genre[0].split('/') for genre in genres]
    # genres = list(set([j for i in genres for j in i]))
    # print(genres)
    query = ("SELECT DISTINCT Genre FROM Genre")
    genres1 = sqlGetter(query)
    # genres1 = [genre[0].split('/') for genre in genres1]
    # genres1 = list(set([j for i in genres1 for j in i]))
    # print(genres1)
    query = ("SELECT idMovie, MovieName FROM Movie")
    movies = sqlGetter(query)
    print(genres1)
    return render_template('genre.html',genres=genres, genres1=genres1, movies=movies, tag=user)

@app.route('/genre/addGenre', methods=["POST"])
def adminAddGenre():
    global user
    query = ("insert into Genre values (%s, %s)")
    data = (request.form["genreName"],request.form["movieID"])
    sqlSetter1(query,data)
    return redirect(url_for('genrePage'))

@app.route('/genre/removeGenre', methods=["POST"])
def adminRemoveGenre():
    global user
    query = ("DELETE FROM Genre WHERE Genre=%s")
    data = (request.form["genreType"],)
    sqlSetter1(query,data)
    return redirect(url_for('genrePage'))

@app.route('/genre/editGenreforMovie', methods=["POST"])
def adminEditGenre():
    global user
    query = ("SELECT * FROM Genre WHERE Genre=%s AND Movie_idMovie=%s")
    data = (request.form["genreType"],request.form["movieID"])
    rst = sqlGetter1(query,data)
    if len(list(sum(rst, ()))) == 0:
        query = ("INSERT INTO Genre VALUES (%s, %s)")
        sqlSetter1(query,data)
    else:
        query = ("DELETE FROM Genre WHERE Genre=%s AND Movie_idMovie=%s")
        sqlSetter1(query,data)
    return redirect(url_for('genrePage'))


###################################################
@app.route('/room')
def roomPage():
    global user
    query = ("SELECT * FROM TheatreRoom")
    rooms = sqlGetter(query)
    return render_template('room.html',rooms=rooms, tag=user)

@app.route('/room/addRoom', methods=["POST"])
def adminAddRoom():
    query = (
        "INSERT IGNORE INTO TheatreRoom VALUES (%s, %s)"
    )
    data = (request.form["roomNo"], request.form["capacity"] )
    sqlSetter1(query, data)
    return redirect(url_for('roomPage'))

@app.route('/room/removeRoom', methods=["POST"])
def adminRemoveRoom():
    query = (
         "DELETE FROM TheatreRoom WHERE RoomNumber=%s"
    )
    data = (request.form["roomNo"],)
    sqlSetter1(query,data)
    return redirect(url_for('roomPage'))

@app.route('/room/editRoom', methods=["POST"])
def adminEditRoom():
    query = (
         "UPDATE TheatreRoom SET Capacity=%s WHERE RoomNumber=%s"
    )
    data = (request.form["capacity"],request.form["roomNo"])
    sqlSetter1(query,data)
    return redirect(url_for('roomPage'))

###################################################
@app.route('/attend')
def attendPage():
    global user
    query = (
        "select idShowing, MovieName, ShowingDateTime, FirstName, LastName, Rating from "
        "Attend a left outer join Customer c on a.Customer_idCustomer = c.idCustomer "
        "left outer join Showing s on a.Showing_idShowing = s.idShowing "
        "left outer join Movie m on s.Movie_idMovie = m.idMovie;"
    )
    attends = sqlGetter(query)
    return render_template('attend.html', attends=attends, tag=user)

@app.route('/attend/<attendKey>', methods=["POST"])
def attendSortBy(attendKey):
    global user
    query = (
        "select idShowing, MovieName, ShowingDateTime, FirstName, LastName, Rating from "
        "Attend a left outer join Customer c on a.Customer_idCustomer = c.idCustomer "
        "left outer join Showing s on a.Showing_idShowing = s.idShowing "
        "left outer join Movie m on s.Movie_idMovie = m.idMovie "
        "order by " + attendKey
    )
    attends = sqlGetter(query)
    return render_template('attend.html', attends=attends, tag=user)


###################################################
def sqlGetter(query):
    cnx = mysql.connector.connect(user='root', password='wzd0606', database='MovieTheatre')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    res = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return res

def sqlSetter(query):
    cnx = mysql.connector.connect(user='root', password='wzd0606', database='MovieTheatre')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    cnx.commit()
    cnx.close()

def sqlGetter1(query, data=None):
    cnx = mysql.connector.connect(user='root', password='wzd0606', database='MovieTheatre')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, data)
    res = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return res

def sqlSetter1(query, data):
    print("in sql1")
    cnx = mysql.connector.connect(user='root', password='wzd0606', database='MovieTheatre')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, data)
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    print("Hello")
    app.run(host="localhost", debug=True)

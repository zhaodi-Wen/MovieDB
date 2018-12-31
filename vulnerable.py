from flask import Flask, render_template, redirect, url_for, request, render_template_string, g
import mysql.connector

app = Flask(__name__)

@app.route("/")
def main():
    query = ("SELECT * FROM Showing s LEFT OUTER JOIN Movie m ON s.Movie_idMovie = m.idMovie;")
    showings = sqlGetter(query)
    query = ("SELECT DISTINCT Genre FROM Genre")
    genres = sqlGetter(query)
    query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
    dates = sqlGetter(query)
    query = ("SELECT idCustomer, FirstName, LastName FROM Customer WHERE NOT (FirstName='Super' AND LastName='User') ")
    customers = sqlGetter(query)
    return render_template('showingVulnerable.html', showings=showings, genres=genres, customers=customers, dates=dates)

@app.route('/showing/search', methods=["POST"])
def showingSearch():
    query = (
        "SELECT * FROM Showing "
        "LEFT OUTER JOIN Movie "
        "ON Movie_idMovie = idMovie "
        "LEFT OUTER JOIN Genre "
        "ON idMovie = Genre.Movie_idMovie "
        "WHERE Genre = %s "
        "AND ShowingDateTime > %s "
        "AND ShowingDateTime < %s "
        "AND MovieName like '" + request.form['movieName'] + "'"
    )
    data = (request.form['genre'], request.form['startDate'], request.form['endDate'])
    showings = sqlGetter1(query, data)
    query = ("SELECT DISTINCT Genre FROM Genre")
    genres = sqlGetter(query)
    query = ("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime")
    dates = sqlGetter(query)
    return render_template('showingVulnerable.html', showings=showings, genres=genres, dates=dates)

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
    cnx = mysql.connector.connect(user='root', password='wzd0606', database='MovieTheatre')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, data)
    cnx.commit()
    cnx.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

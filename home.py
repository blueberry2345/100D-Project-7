import sqlite3
from cafe import Cafe
from flask import Flask, render_template, request, redirect, url_for

# Connect to database.
cafe_db = sqlite3.connect('cafes.db', check_same_thread=False)
cursor = cafe_db.cursor()
cafes_data = cursor.execute("SELECT * from cafe").fetchall()

# Create list of cafe objects using the database contents and record the number of the last cafe.
last_num = 0
cafes = []
for cafe in cafes_data:
    new_cafe = Cafe(cafe[1], cafe[2], cafe[3], cafe[4], cafe[5],
                    cafe[6], cafe[7], cafe[8], cafe[9], cafe[10])
    cafes.append(new_cafe)
    last_num = cafe[0]

# Create Flask app.
app = Flask(__name__)

# Establish the home page.
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", cafes=cafes)


# Route for users to add a cafe which is added to the existing list and added to the database file.
@app.route("/add_cafe", methods=['POST'])
def add():
    if request.method == 'POST':
        cafe_name = request.form['name_entry']
        cafe_map = request.form['map_entry']
        cafe_picture = request.form['picture_entry']
        cafe_location = request.form['location_entry']
        cafe_sockets = request.form.getlist("sockets")
        cafe_toilets = request.form.getlist("toilets")
        cafe_wifi = request.form.getlist("wifi")
        cafe_calls = request.form.getlist("calls")
        cafe_seats = request.form["seats"]
        cafe_coffee = request.form["coffee"]
        new_cafe = Cafe(cafe_name, cafe_map, cafe_picture, cafe_location, cafe_sockets, cafe_toilets, cafe_wifi,
                        cafe_calls, cafe_seats, cafe_coffee)
        cafes.append(new_cafe)
        cursor.execute('''
           INSERT INTO cafe (id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)
           ''', (
            (last_num + 1), cafe_name, cafe_map, cafe_picture, cafe_location, str(cafe_sockets), str(cafe_toilets),
            str(cafe_wifi), str(cafe_calls), cafe_seats, cafe_coffee))
        cafe_db.commit()
    return redirect(url_for('home'))


# Route that allows users to remove a cafe from the list and database
@app.route("/remove_cafe", methods=['POST'])
def remove():
    remove_cafe = request.form.get("delete")
    for cafe in cafes:
        if cafe.name == remove_cafe:
            cafes.remove(cafe)
            cursor.execute('''
            DELETE FROM cafe
            WHERE name = ?
            ''', (cafe.name,)
            )
            cafe_db.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)


cafe_db.close()

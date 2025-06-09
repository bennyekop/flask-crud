# app.py


from flask import Flask, render_template, request, redirect, url_for, flash

from flask_mysqldb import MySQL

from dotenv import load_dotenv

import os


# Load environment variables from .env file

load_dotenv()


app = Flask(__name__)


# Flask Session configuration (for flash messages)

app.secret_key = os.getenv('SECRET_KEY')


# MySQL Configurations

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')

app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')

app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


mysql = MySQL(app)


# --- Routes ---


@app.route('/')

def index():

    """

    Renders the main page, displaying a list of all users from the database.

    Also provides a form to add new users.

    """

    try:

        cur = mysql.connection.cursor()

        # Execute SQL query to fetch all users

        cur.execute("SELECT * FROM users")

        users = cur.fetchall() # Fetch all rows from the query result

        cur.close()

        return render_template('index.html', users=users)

    except Exception as e:

        flash(f"Error fetching users: {e}", 'danger')

        return render_template('index.html', users=[])


@app.route('/add_record', methods=['POST'])

def add_record():

    """

    Handles the submission of the 'add user' form.

    Inserts a new user record into the database.

    """

    if request.method == 'POST':

        try:

            # Get form data

            name = request.form['name']

            email = request.form['email']

            phone = request.form['phone']


            cur = mysql.connection.cursor()

            # Execute SQL INSERT statement

            cur.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))

            mysql.connection.commit() # Commit changes to the database

            cur.close()

            flash("User added successfully!", 'success')

            return redirect(url_for('index'))

        except Exception as e:

            # Rollback in case of error

            mysql.connection.rollback()

            flash(f"Error adding user: {e}", 'danger')

            return redirect(url_for('index'))


@app.route('/edit_record/<int:id>')

def edit_record(id):

    """

    Renders the edit form for a specific user.

    Fetches the user details from the database based on the provided ID.

    """

    try:

        cur = mysql.connection.cursor()

        # Fetch a single user by ID

        cur.execute("SELECT * FROM users WHERE id = %s", (id,))

        user = cur.fetchone() # Fetch single row

        cur.close()

        if user:

            return render_template('edit.html', user=user)

        else:

            flash("User not found!", 'danger')

            return redirect(url_for('index'))

    except Exception as e:

        flash(f"Error fetching user for edit: {e}", 'danger')

        return redirect(url_for('index'))


@app.route('/update_record/<int:id>', methods=['POST'])

def update_record(id):

    """

    Handles the submission of the 'edit user' form.

    Updates an existing user record in the database.

    """

    if request.method == 'POST':

        try:

            # Get form data

            name = request.form['name']

            email = request.form['email']

            phone = request.form['phone']


            cur = mysql.connection.cursor()

            # Execute SQL UPDATE statement

            cur.execute("UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, id))

            mysql.connection.commit()

            cur.close()

            flash("User updated successfully!", 'success')

            return redirect(url_for('index'))

        except Exception as e:

            mysql.connection.rollback()

            flash(f"Error updating user: {e}", 'danger')

            return redirect(url_for('index'))


@app.route('/delete_record/<int:id>', methods=['POST'])

def delete_record(id):

    """

    Handles the deletion of a user record.

    Deletes a user from the database based on the provided ID.

    """

    try:

        cur = mysql.connection.cursor()

        # Execute SQL DELETE statement

        cur.execute("DELETE FROM users WHERE id = %s", (id,))

        mysql.connection.commit()

        cur.close()

        flash("User deleted successfully!", 'success')

        return redirect(url_for('index'))

    except Exception as e:

        mysql.connection.rollback()

        flash(f"Error deleting user: {e}", 'danger')

        return redirect(url_for('index'))


if __name__ == '__main__':

    # Flask development server by default binds to 127.0.0.1 (localhost).

    # To make it accessible from outside the container, bind to 0.0.0.0.

    app.run(host='0.0.0.0', debug=True)

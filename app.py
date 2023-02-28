import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET KEY'] = '26e3e28801be26f8bb15ca5905db503c8bc0719f5ddda75f'

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_shoes(shoe_id):
    conn = get_connection()
    shoes = conn.execute("SELECT * FROM products WHERE id = ?", (shoe_id,)).fetchone()
    conn.close()

    if shoes is None:
        abort(404)
    return shoes

@app.route('/')
def index():
    conn = get_connection()
    shoes = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', shoes=shoes)

@app.route('/input/', methods=('GET', 'POST'))
def add():
    if request.method == "POST":
        title = request.form['title']
        image = request.form['image']
        price = request.form['price']
        if not title:
            flash("title is required")
        elif not price:
            flash("price is required")
        elif not image:
            flash("image URL is required")
        else:
            conn = get_connection()
            conn.execute('INSERT INTO products (title, image, price) VALUES (?, ?, ?)', (title, image, price))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('input.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    shoes = get_shoes(id)
    if request.method == 'POST':
        title = request.form["title"]
        image = request.form["image"]
        price = request.form["price"]

        if not title:
            flash('title required')
        elif not image:
            flash("Image URL required")
        elif not price:
            flash("Price required")

        else:
            conn = get_connection()
            conn.execute('UPDATE products SET title = ?, image = ?, price = ?'
                         ' WHERE id = ?',
                         (title, image, price, id))
            conn.commit()
            return redirect(url_for('index'))

    return render_template("edit.html", shoes=shoes)

@app.route('/<int:id>/delete/', methods=('GET','POST'))
def delete(id):
    shoes = get_shoes(id)
    conn = get_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    if shoes is not None:
        flash('"{}" was successfully deleted!'.format(shoes['title']))
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()

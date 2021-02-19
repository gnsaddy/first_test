from flask import Flask, render_template, json, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "qwertyuiop"


@app.route('/', methods=["GET", "POST"])
def index():
    task = 0.0
    if request.method == "POST":
        try:
            amb = request.form["amb"]
            queue = request.form["queue"]
            amount = request.form["amount"]

            state = request.form["state"]
            reason = request.form["reason"]
            print(amount)
            with sqlite3.connect("testFirst.db") as con:

                if int(amount) > int(0):
                    task = 1.0
                elif int(amount) == int(0):
                    task = 0.5
                cur = con.cursor()
                cur.execute("INSERT into test (amb, queue, amount,"
                            "task, state, reason) values (?,?,?,?,?,?)",
                            (amb, queue, amount, task, state, reason))
                con.commit()
                flash("Data inserted successfully!!")
            return redirect(url_for('index'))
        except TypeError:
            con.rollback()
            flash("Data not inserted!!")
    else:
        # flash("Data not inserted!!")
        con = sqlite3.connect("testFirst.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * from test")
        get_rows = cur.fetchall()
        return render_template('index.html', data=get_rows)


@app.route("/display")
def display():
    con = sqlite3.connect("testFirst.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from test")
    get_rows = cur.fetchall()

    return render_template('display.html', data=get_rows)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        aid = request.form["aid"]
        queue = request.form["queue"]
        with sqlite3.connect("testFirst.db") as con:
            try:
                cur = con.cursor()
                if aid:
                    cur.execute("select amb from test where amb=?", (aid,))
                    get_rows = cur.fetchall()
                    if get_rows:
                        cur.execute("delete from test where amb = ?", (aid,))
                        flash("deleted!!")
                        return redirect(url_for('display'))
                    else:
                        flash("Amb id does not matched!!")
                        return redirect(url_for('delete'))
                elif queue:
                    cur.execute("select queue from test where queue=?", (queue,))
                    get_rows = cur.fetchall()
                    if get_rows:
                        cur.execute("delete from test where queue = ?", (queue,))
                        flash("deleted!!")
                        return redirect(url_for('display'))
                    else:
                        flash("Queue id does not matched!!")
                        return redirect(url_for('delete'))
                return redirect(url_for('display'))
            except TypeError:
                flash("Can not delete!!")
    else:
        return render_template('delete.html')


@app.route("/display/update/<int:uid>", methods=["GET", "POST"])
def update(uid):
    con = sqlite3.connect("testFirst.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from test where id = ?", (uid,))
    get_rows = cur.fetchall()

    if request.method == "POST":

        try:
            amb = request.form["amb"]
            queue = request.form["queue"]
            amount = request.form["amount"]
            task = request.form["task"]
            state = request.form["state"]
            reason = request.form["reason"]

            with sqlite3.connect("testFirst.db") as con:
                cur = con.cursor()
                cur.execute("update test set amb=?, queue=?,amount=?,task=?,state=?,reason=? where id=?",
                            (amb, queue, amount, task, state, reason, uid))

                con.commit()
                flash("Data updated successfully!!")
            return redirect(url_for('display'))
        except TypeError:
            con.rollback()
            flash("Database error!!")

    return render_template('update.html', data=get_rows)


@app.route('/search', methods=["POST", "GET"])
def search():
    aid = request.form.get('aid')
    con = sqlite3.connect("testFirst.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from test where amb = ? or queue = ? or state = ?", (aid, aid, aid))
    get_rows = cur.fetchall()

    return render_template('search.html', data=get_rows)


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "Shhhh!"

db = SQLAlchemy(app)

class Items(db.Model):

    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    priority = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer)

    def __init__(self, task, priority, status):
        self.task = task
        self.priority = priority
        self.status = status

    def __repr__(self):
        return '<task %r>' % (self.body)

@app.route('/', methods=['GET'])
def home():
    open_items = db.session.query(Items).filter_by(status='1')
    closed_items = db.session.query(Items).filter_by(status='0')
    return render_template('home.html',open_items=open_items, closed_items=closed_items)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    priority = request.form['priority']
    if not task or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('home'))   
    else:
        new_item = Items(
                    task,
                    priority,
                    '1'
                    )
        db.session.add(new_item)
        db.session.commit()
        flash('New task entered!')
        return redirect(url_for('home'))

@app.route('/complete/<int:item_id>')
def complete(item_id):
    new_id = item_id
    db.session.query(Items).filter_by(item_id = new_id).update({"status":"0"})
    db.session.commit()
    flash('Completed!')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)




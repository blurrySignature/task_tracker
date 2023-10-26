from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


def get_db_connection_url():
    load_dotenv()
    db_user = os.getenv('PG_USER')
    db_password = os.getenv('PG_PASSWORD')
    db_name = os.getenv('PG_DBNAME')
    db_host = os.getenv('HOST')
    db_port = os.getenv('PORT')
    return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_url()
db = SQLAlchemy(app)


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, server_default=db.text('false'))
    date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/tasks', methods=['GET'])
def get_records():
    records_list = Record.query.order_by(Record.date).all()
    return render_template('tasks.html', records_list=records_list)


@app.route('/tasks', methods=['POST'])
def create_record():
    note_text = request.form['TextareaForCreateRecord']
    if note_text:
        new_record = Record(note=note_text)
        try:
            db.session.add(new_record)
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'Error'
    else:
        return redirect('/tasks')


@app.route('/tasks/update/<int:record_id>', methods=['POST'])
def update_record(record_id):
    record = Record.query.get_or_404(record_id)
    note_text = request.form.get('TextareaForUpdateRecord')
    if note_text:
        record.note = note_text
    else:
        record.is_completed = not record.is_completed
    try:
        db.session.commit()
    except:
        return 'Error'
    return redirect('/tasks')


@app.route('/tasks/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = Record.query.get_or_404(record_id)
    if record:
        try:
            db.session.delete(record)
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'Error'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', debug=True, port=8000)

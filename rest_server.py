import os
from flask import Flask, url_for, jsonify, abort, make_response, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_marshmallow import Marshmallow

DB_FILENAME = 'app.db'
DEBUG = True

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_FILENAME)
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    # description = db.Column(db.String(120), unique=False, nullable=True)
    done = db.Column(db.Boolean, unique=False, default=False)


if not os.path.exists(DB_FILENAME):
    db.create_all()


class TasksSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tasks

    id = ma.auto_field()
    title = ma.auto_field()
    # description = ma.auto_field()
    done = ma.auto_field()


task_schema = TasksSchema()
tasks_schema = TasksSchema(many=True)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = tasks_schema.dump(Tasks.query.all())
    return jsonify({'tasks': [*map(make_public_task, tasks)]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = task_schema.dump(Tasks.query.filter_by(id=task_id).first())
    if not task:
        abort(404)
    return jsonify({'task': make_public_task(task)})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not ('title' in request.json):
        abort(400)
    task = Tasks(
        title=request.json['title'],
        # description=request.json.get('description', '')
    )
    try:
        db.session.add(task)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session().rollback()
        abort(400)
    task = task_schema.dump(task)
    return jsonify({'task': make_public_task(task)}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    # if 'description' in request.json and not isinstance(request.json['description'], str):
    #     abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    task.title = request.json.get('title', task.title)
    # task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    task = task_schema.dump(task)
    return jsonify({'task': make_public_task(task)})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})


if __name__ == '__main__':
    if DEBUG:
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)

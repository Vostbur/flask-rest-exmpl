from flask import Flask, url_for, jsonify, abort, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

from tasks_data_for_testing import tasks

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'alex':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


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
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [*map(make_public_task, tasks)]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    # task = list(filter(lambda t: t['id'] == task_id, tasks))
    # or
    # task = [i for i in tasks if i['id'] == task_id]
    # if len(task) == 0:
    #     abort(404)
    # return jsonify({'task': task[0]})
    task = next((i for i in tasks if i['id'] == task_id), False)
    if not task:
        abort(404)
    return jsonify({'task': make_public_task(task)})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not ('title' in request.json):
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = next((i for i in tasks if i['id'] == task_id), False)
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json and not isinstance(request.json['description'], str):
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify({'task': make_public_task(task)})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = next((i for i in tasks if i['id'] == task_id), False)
    if not task:
        abort(404)
    tasks.remove(task)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)

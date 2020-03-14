import os.path
from todo_app import db, Tasks


if not os.path.exists('app.db'):
    db.create_all()

    test_task_1 = Tasks(title='Buy something', description='milk, cheese, pizza')
    test_task_2 = Tasks(title='Learn python', description='find good tutorial')

    db.session.add(test_task_1)
    db.session.add(test_task_2)
    db.session.commit()

all_task = Tasks.query.all()
task_2 = Tasks.query.filter_by(id=2).first()

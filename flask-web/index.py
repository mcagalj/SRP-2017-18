from flask import Flask, request, render_template, \
    redirect, url_for, session, g, jsonify

from os import urandom
from utils import User, find_user, requires_login, requires_roles

app = Flask(__name__)


@app.before_request
def set_user():
    g.user = None
    if 'username' in session:
        g.user = {
            'name': session['username'],
            'role': session['role']
        }


@app.before_request
def log_requests():
    if g.user:
        print(g.user)
        app.logger.info(
            '"{1}" (role: "{2}") ==> {0}'.format(
                request.path,
                g.user['name'],
                g.user['role']
            )
        )
    else:
        app.logger.info('Requested path {}'.format(request.path))


@app.route('/')
def index():
    if g.user:
        return render_template('index.html', name=g.user['name'])
    return redirect(url_for('login'))


@app.route('/admin')
@requires_login
@requires_roles('admin')
def admin_page():
    return render_template('restricted.html', role='admin')


@app.route('/tester')
@requires_login
@requires_roles('admin', 'tester')
def tester_page():
    return render_template('restricted.html', role='tester')

# ============== Lab BEGIN ====================


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route('/api/tasks', methods=['GET'])
@requires_login
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return('Requested task does not exist')
    return jsonify({'task': task[0]})


# @app.route('/api/tasks', methods=['POST'])
@app.route('/api/tasks/add', methods=['GET'])
def create_task():
    id = len(tasks) + 1

    task = {
        'id': id,
        'title': 'New item {0}'.format(id),
        'description': 'New task to do',
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task})


# @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@app.route('/api/tasks/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return('Requested task does not exist')
    tasks.remove(task[0])
    return jsonify({'task': task[0]})
# ============== Lab END ======================


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = find_user(request.form['username'], users=USERS)
        if user and user.verify_password(request.form['password']):
            app.logger.info('User "{}" logged in'.format(user.username))
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('index'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route('/logout')
@requires_login
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404


if __name__ == '__main__':
    ''' The server component that comes with Flask is really
    only meant for when you are developing your application;
    even though it can be configured to handle concurrent requests
    (with app.run(threaded=True)).

    https://stackoverflow.com/questions/14672753/handling-multiple-requests-in-flask
    '''

    # Let us create some users.
    USERS = (
        User('iivic', 'ivana', 'tester'),
        User('pperic', 'petar', 'admin'),
        User('mmatic', 'mate', 'user'),
        User('mmijic', 'mia', 'admin')
    )

    # print('-'*80)
    # for user in USERS:
    #     print('{0:>2} {1}'.format('*', user))
    # print('-'*80)

    app.config['TITLE'] = 'Security @ FESB'
    app.secret_key = urandom(24)
    app.run(host='127.0.0.1', port=8000, threaded=True, debug=True)

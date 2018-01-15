from flask import request, redirect, url_for, flash, g
from functools import wraps
from passlib.hash import sha256_crypt as crypt
from passlib import pwd

# ROLES = ('user', 'admin', 'tester')
# ROLES_PERMS = {
#     'user': ('read'),
#     'admin': ('read', 'add', 'delete'),
#     'tester': ('read', 'add')
# }
# print('write' in ROLES_PERMS['admin'])
# print('write' in ROLES_PERMS['user'])


class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.hash = crypt.encrypt(password, salt=pwd.genword(16), rounds=5000)
        self.role = role

    def verify_password(self, password):
        return crypt.verify(password, self.hash)

    def __str__(self):
        return "User: ({},{},{})".format(
            self.username,
            self.hash,
            self.role
        )


def requires_login(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if g.user:
            return f(*args, **kwargs)
        flash('Unauthenticated request to {}.'.format(request.path))
        return redirect(url_for('login'))
    return wrapped


def get_user_role():
    if g.user:
        return g.user.get('role', None)
    return None


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_role() in roles:
                return f(*args, **kwargs)
            flash('Unauthorized request to {}.'.format(request.path))
            flash('This page requires role/s: {}'.format(roles))
            return redirect(url_for('index'))
        return wrapped
    return wrapper


def find_user(username, users=()):
    for user in users:
        if user.username == username:
            return user
    return None

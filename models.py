from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

import time
import shutil


db_path = 'db.sqlite'

app = Flask(__name__)

app.secret_key = 'random string'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    created_time = db.Column(db.String())
    sex = db.Column(db.String())
    note = db.Column(db.String())
    role = db.Column(db.Integer, default=2)
    # 这是引用别的表的数据的属性，表明了它关联的东西
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.sex = form.get('sex', '')
        self.note = form.get('note', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def json(self):
        self.id
        d = {k: v for k, v in self.__dict__.items() if k is not '_sa_instance_state'}
        return d

    # def __str__(self):
    #     class_name = self.__class__.__name__
    #     return u'<ID:{} Username:{} Sex:{} Role:{}>'\
    #         .format(self.id, self.username, self.sex, self.role)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def valid(self):
        username_len = len(self.username) >= 3
        password_len = len(self.password) >= 3
        return username_len and password_len

    def validate(self, user):
        if isinstance(user, User):
            username_equals = self.username == user.username
            password_equals = self.password == user.password
            return username_equals and password_equals
        else:
            return False


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.String())
    # 这是一个外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def json(self):
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in ('_sa_instance_state', 'user')}
        return d

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.String())

    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.blog_id = form.get('blog_id', '')
        self.created_time = ''

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def json(self):
        self.id
        d = {k: v for k, v in self.__dict__.items() if k is not '_sa_instance_state'}
        return d

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String())
    created_time = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.todo = form.get('todo', '')
        self.created_time = ''

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def backup_db():
    backup_path = '{}.{}'.format(time.time(), db_path)
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    # rebuild_db()
    pass

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session
from flask import abort

from models import User
from models import Blog
from models import Comment

import random
import time


app = Flask(__name__)

app.secret_key = 'lxx'


def log(*args):
    t = time.time()
    tt = time.strftime(r'%Y/%m/%d %H:%M:%S', time.localtime(t))
    print(tt, *args)
    with open('log.txt', 'a') as f:
        f.write('{} : {}\n'.format(tt, *args))
        f.close()


def current_user():
    # cid = request.cookies.get('cookie_id', '')
    # user = cookie_dict.get(cid, None)
    user_id = session.get('user_id', '')
    user = User.query.filter_by(id=user_id).first()
    return user


def parse_comment(content):
    c =['<p>{}</p>'.format(i) for i in content.split('\n')]
    log('test c :', c)
    result = b''
    for i in c:
        result += i
    return result

env = app.jinja_env
env.filters['parse_comment'] = parse_comment


@app.route('/', methods=['GET'])
def root_view():
    # 为防止直接访问根路径产生404，设置一次跳转
    u = current_user()
    if u is None:
        id_of_mine = 1
        user_id = id_of_mine
    else:
        user_id = u.id
    return redirect(url_for('blogs_view', user_id=user_id))


@app.route('/<user_id>', methods=['GET'])
def blogs_view(user_id):
    u = current_user()
    arg ={}
    other_blogs = []
    if u is None:
        id_of_mine = 1
        # 当前没用户登录，默认加载自己的(id=1)blog
        blogs = Blog.query.filter_by(user_id=id_of_mine).all()
        user = User.query.filter_by(id=id_of_mine).first()
        arg['current_user_id'] = False
    else:
        # 当前有用户登录，加载动态路由中的user_id对应的用户blog
        blogs = Blog.query.filter_by(user_id=user_id).all()
        user = User.query.filter_by(id=user_id).first()
        arg['current_user_id'] = u.id
    blogs.sort(key=lambda t: t.created_time, reverse=True)
    log('待加载的博客:', [i.content for i in blogs])
    total_blog_num = len(Blog.query.all())
    for i in range(8):
        random_id = random.randint(1, total_blog_num)
        other_blog = Blog.query.filter_by(id=random_id).first()
        other_blogs.append(other_blog)
    arg['other_blogs'] = other_blogs
    arg['blogs'] = blogs[:3]
    arg['user'] = user
    for blog in arg['blogs']:
        blog.content = blog.content[:200]
    log('index current user is', arg['current_user_id'])
    return render_template('index.html', **arg)

# {'title': '555555555555555', 'id': 5, 'user': <User: 1>, 'created_time': '1474033266.74831', 'content': '### Hello Editor.md !\n555555555555555555555555555555', 'user_id': 1}
# {'user_id': 1, 'content': '### Hello Editor.md !\n2222222222222222222', 'title': '2222222222222', 'created_time': '1474031806.26777', 'id': 2}
@app.route('/api/<user_id>', methods=['GET'])
def blogs_api(user_id):
    args = request.args
    offset = args.get('offset', 0)
    limit = args.get('limit', 3)
    offset = int(offset)
    limit = int(limit)
    u = current_user()
    arg ={}
    if u is None:
        id_of_mine = 1
        # 当前没用户登录，默认加载自己的(id=1)blog
        blogs = Blog.query.filter_by(user_id=id_of_mine).all()
        user = User.query.filter_by(id=id_of_mine).first()
        arg['current_user_id'] = False
    else:
        # 当前有用户登录，加载动态路由中的user_id对应的用户blog
        blogs = Blog.query.filter_by(user_id=user_id).all()
        user = User.query.filter_by(id=user_id).first()
        arg['current_user_id'] = u.id
    blogs.sort(key=lambda t: t.created_time, reverse=True)
    # 本次拿出的博客，转化为字典
    blogs_to_show = blogs[offset:offset + limit]
    # log('debugdebugdebugdebug!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', blogs[0].json())
    arg['blogs'] = [blog.json() for blog in blogs_to_show]
    # log('debugdebugdebugdebug!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', arg['blogs'][0])
    arg['user'] = user.json()
    arg['user']['blogs'] = [b.json() for b in arg['user']['blogs']]
    # 缩略页显示二百个字符
    for blog in arg['blogs']:
        blog['content'] = blog['content'][:200]
    # log('index current user is', arg['current_user_id'])
    # log('debugdebugdebugdebug!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', arg)
    return jsonify(arg)


@app.route('/register', methods=['POST'])
def register():
    # 如果没注册过，就注册后再跳转，如果注册过了，就直接跳转
    form = request.form
    log('debug form:', form)
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is None:
        # user为空，没注册过
        u.save()
        session['user_id'] = u.id
        return redirect(url_for('blogs_view', user_id=u.id))
    else:
        # user不为空，注册过
        if user.validate(u):
            # 验证账户密码通过
            log("用户登录成功", user, user.username, user.password)
            session['user_id'] = user.id
            log('debug userid', user.id)
            r = redirect(url_for('blogs_view', user_id=user.id))
            return r
        else:
            log('账号名或密码错误')
            id_of_mine = 1
            return redirect(url_for('blogs_view', user_id=id_of_mine))


@app.route('/logout')
def logout():
    u = current_user()
    if u is not None:
        log('current usr is', u.id, u.username)
        session.pop('user_id')
    r = dict(
        success=True,
        url=url_for('root_view')
    )
    return jsonify(r)


@app.route('/about', methods=['GET'])
def profile_view():
    u = current_user()
    if u is not None:
        user_id = u.id
    else:
        user_id = False
    return render_template('aboutme.html', user_id=user_id)


@app.route('/blog/details/<blog_id>', methods=['GET'])
def blog_detail_view(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        user = current_user()
        # user = blog.user
        log('debug', comments)
        arg = dict(
            blog=blog,
            comments=comments,
            user=user
            # user=user
        )
        log('发回前端的文章内容，查看一下格式问题:',blog.content)
    else:
        abort(404)
    return render_template('blog_detail.html', **arg)


@app.route('/blog/comments/add', methods=['POST'])
def blog_comment_add():
    form = request.get_json()
    comment = Comment(form)
    comment.created_time = time.time()
    u = current_user()
    log('debug current user:', u)
    if u is not None:
        comment.user_id = u.id
        comment.save()
        current_username = u.username
        response = {
            'success': True,
            'title': comment.title,
            'content': comment.content,
            'created_time': comment.created_time,
            'username': current_username,
        }
    else:
        response = {
            'success': False,
        }
    return jsonify(response)


@app.route('/editor/<user_id>')
def editor_view(user_id):
    return render_template('editor.html', user_id=user_id)


@app.route('/blog/add', methods=['POST'])
def blog_add():
    form = request.get_json()
    log('发回的md格式文章：',form)
    blog = Blog(form)
    blog.created_time = time.time()
    blog.save()
    response = {
        'id': blog.id,
        'success': True,
        'title': blog.title,
        'content': blog.content,
        'created_time': blog.created_time,
    }
    log('发回前端的文章信息:', jsonify(response))
    return jsonify(response)


    #
    # @app.route('/blog/comments', methods=['POST'])
    # def blog_comment():
    #     title = request.form.get('title','')
    #     content = request.form.get('content', '')
    #     print('form:',request.form)
    #     print('args:',request.args)
    #     print('title : ',title,'\ncontent : ', content)
    #     # return redirect(url_for('blog_detail_view'))
    #     r = '\ntitle:{}\ncontent:{}'.format(title, content)
    #     return jsonify(r)

if __name__ == '__main__':
    app.run(debug=True)
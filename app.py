from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session

from models import User
from models import Blog
from models import Comment

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
    user_id = session['user_id']
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
def blogs_view():
    # blog = Blog.query.filter_by(id=1).first()
    # print('debug', blog)
    blog = 'adsfadsfa sdfasdfasdfadsfads fasdfas dfasdfa dsfadsfasdfasdfa sdfadsfadsfasdf asdfasdfadsfa dsfasdfasdfasd fadsfadsfas dfasdfas dfadsfadsf asdfasdfa sdfadsf adsfasdfa sdfasdfadsfad sfasdfasdf asdfadsfadsfasdfasdf asdfad sfadsfasdfasdfasd fadsfa d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads '
    return render_template('index.html', blog=blog[:200])


@app.route('/about', methods=['GET'])
def profile_view():
    return render_template('aboutme.html')


@app.route('/blog/details', methods=['GET'])
def blog_detail_view():
    # blog = Blog.query.filter_by(id=blog_id).first()
    comments = Comment.query.filter_by(blog_id=1).all()
    log('debug', comments)
    # log('test created_time:', comments[-1].created_time, comments[-1].id)
    return render_template('blog_detail.html', comments=comments)


@app.route('/blog/comments/add', methods=['POST'])
def blog_comment_add():
    form = request.get_json()
    log('!!!!!!!!!!!!test form :',form)
    comment = Comment(form)
    comment.created_time = time.time()
    comment.save()
    log('!!!!!!!!!!!!test content :',comment)
    response = {
        'success': True,
        'title': comment.title,
        'content': comment.content,
        'created_time': comment.created_time
    }
    return jsonify(response)


@app.route('/register')
def register():
    form = request.form
    log('debug form:', form)
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is None:
        u.save()
        return redirect(url_for('editor_view', user_id=u.id))
    else:
        if user.validate(u):
            log("用户登录成功", user, user.username, user.password)
            session['user_id'] = user.id
            r = redirect(url_for('editor_view', user_id=user.id))
            return r
        else:
            log('账号名或密码错误')
            return redirect(url_for('blogs_view'))





            # # 用 make_response 生成响应 并且设置 cookie
            # r = make_response(redirect(url_for('editor_view', user_id=u.id)))
            # # cookie_id = str(uuid.uuid4())
            # # cookie_dict[cookie_id] = user
            # session['user_id'] = user.id
            # r.set_cookie('cookie_id', cookie_id)


@app.route('/editor/<user_id>')
def editor_view(user_id):
    return render_template('editor.html', user_id=user_id)

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
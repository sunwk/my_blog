from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify

from models import Blog
from models import Comment

import time


app = Flask(__name__)


@app.route('/', methods=['GET'])
def blogs_view():
    # blog = Blog.query.filter_by(id=1).first()
    # print('debug', blog)
    blog = 'adsfadsfa sdfasdfasdfadsfads fasdfas dfasdfa dsfadsfasdfasdfa sdfadsfadsfasdf asdfasdfadsfa dsfasdfasdfasd fadsfadsfas dfasdfas dfadsfadsf asdfasdfa sdfadsf adsfasdfa sdfasdfadsfad sfasdfasdf asdfadsfadsfasdfasdf asdfad sfadsfasdfasdfasd fadsfa d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads d sfasdfasdfas dfads fadsfa d sfasdfasdfas dfads '
    return render_template('index.html', blog=blog[:200])


@app.route('/blog/details', methods=['GET'])
def blog_detail_view():
    # blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('blog_detail.html')


@app.route('/blog/comments/add', methods=['POST'])
def blog_comment_add():
    form = request.get_json()
    print('!!!!!!!!!!!!test form :',form)
    comment = Comment(form)
    comment.save()
    print('!!!!!!!!!!!!test content :',comment)
    response = {
        'success': True,
        'title': comment.title,
        'content': comment.content,
        'created_time': time.time()
    }
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
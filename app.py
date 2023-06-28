from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def fetch_post_by_id(blog_posts, post_id):
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    with open('blog_data.json') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('blog_data.json') as json_file:
            blog_posts = json.load(json_file)
            new_id = blog_posts[-1]['id'] + 1
            new_post = {"id": new_id, "author": request.form["author"],
                        "title": request.form["title"],
                        "like": 0, "content": request.form["content"]}
            blog_posts.append(new_post)
        with open('blog_data.json', 'w') as json_file:
            json.dump(blog_posts, json_file)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('blog_data.json') as json_file:
        blog_posts = json.load(json_file)
        blog_posts = [post for post in blog_posts if post["id"] != post_id]
    with open('blog_data.json', 'w') as json_file:
        json.dump(blog_posts, json_file)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('blog_data.json') as json_file:
        blog_posts = json.load(json_file)
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post["title"] = request.form["title"]
        post["author"] = request.form["author"]
        post["content"] = request.form["content"]
        with open('blog_data.json', 'w') as json_file:
            json.dump(blog_posts, json_file)
        return redirect(url_for('index'))
    return render_template('update.html', post_id=post_id, post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    with open('blog_data.json') as json_file:
        blog_posts = json.load(json_file)
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    else:
        post["like"] += 1
        with open('blog_data.json', 'w') as json_file:
            json.dump(blog_posts, json_file)
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

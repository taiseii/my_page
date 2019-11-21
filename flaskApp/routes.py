import os
from flask import render_template, url_for, flash, redirect, abort, request
from flaskApp import app, db, bcrypt, mail
from flaskApp.forms import loginForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskApp.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
import dash
import dash_html_components as html
from flask_mail import Message


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', page_id=0)


@app.route('/projects')
def projects():
    posts = Post.query.all()
    return render_template('projects.html', page_id=1, posts=posts)


@app.route('/cv')
def cv():
    return render_template('cv.html', page_id=2)


@app.route('/contact')
def contact():
    return render_template('contact.html', page_id=3)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('projects'))
        else: flash('Unsuccessful :(', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('projects.html', page_id=3)


@app.route('/projects/new', methods=['POST', 'GET'])
@login_required
def new_project():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, language=form.language.data,
            category=form.category.data, description=form.description.data,
             author=current_user,link=form.link.data)
        db.session.add(post)
        db.session.commit()
        flash('new project has been successfully added!', 'success')
        return redirect(url_for('projects'))
    return render_template('add_project.html', title='New project', form=form, legend='new project')


@app.route('/projects<int:project_id>')
def a_project(project_id):
    project = Post.query.get_or_404(project_id)
    return render_template('a_project.html', title=project.title, post=project)


@app.route('/projects/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_project(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.language = form.language.data
        post.category = form.category.data
        post.link = form.category.data
        db.session.commit()
        flash('post has been updated', 'success')
        return redirect(url_for('a_project', project_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.language.data = post.language
        form.category.data = post.category
        form.link.data = post.link
    return render_template('add_project.html', title='Update Post', form=form, legend='update post')


@app.route('/projects/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_project(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted', 'success')
    return redirect(url_for('projects'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
        sender='noreply@admin.com', recipients=[user.email])
    msg.body = f'''To reset the password follow the link.
    {url_for('reset_token', token=token, _external=True)}
    '''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('email has been sent with instructions', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password', form=form)


@app.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None :
        flash('invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
     hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
     user.password = hashed_passwd
     db.session.commit()
     flash(f'Password updated you can now login ', 'success')
     return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password', form=form)

# -*- coding: utf-8 -*-
from flask import render_template,request,session,redirect,url_for
from server.views.user import bp
from server.models import db
from server.models.user import User

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        status,ret = Auth(request.form)
        if status:
            session['user_id'] = ret.id
            return redirect(url_for('user.settings'))
        return render_template('login.html',
                email_error=ret[0],
                pw_error=ret[0])
    return render_template('login.html')


@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        status,ret = User.register(request.form['email'],request.form['pw'])
        if status:
            session['user_id'] = ret.id
            return redirect(url_for('user.settings'))
        return render_template('register.html',
                email_error=ret)
    return render_template('register.html')

@bp.route('/settings',methods=['GET','POST'])
def settings():
    return 'hi! {0}'.format(session['user_id'])
def Auth(form):
    return User.login(form['email'],form['pw'])

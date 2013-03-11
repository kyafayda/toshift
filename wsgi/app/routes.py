from flask import render_template, flash, redirect
from flask import session, url_for,request, g
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.login import login_required
from app import app, db, lm, oid
from forms import LoginForm
from forms import PostExpense
from datetime import datetime
from models import User, ROLE_USER, ROLE_ADMIN, Expense


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user  = current_user

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    form = PostExpense()
    if form.validate_on_submit():
        exp = Expense(type = form.type.data, amount = form.amount.data, description = form.description.data, vendor = form.vendor.data, date = datetime.utcnow(), mode = form.mode.data, owner =g.user)
        db.session.add(exp)
        db.session.commit()
        flash('Your expense is posted')
        return redirect(url_for('home'))
    user = g.user
    expenses = g.user.my_expenses().all()
    # #expenses = [
    #         {
    #             'owner': {'nickname': 'Nidhi' },
    #             'expense' : 'Snack'
    #             },
    #         {
    #             'owner' : {'nickname' : 'Vivek' },
    #             'expense' : 'Parking'
    #             }
    #         ]
    return render_template('home.html',
                title = 'Home',
                user  = user,
                form = form,
                expenses = expenses)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
            title = 'Sign In',
            form = form,
            providers = app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email =="":
        flash('Invalid login, Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname =="":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email,
                role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('home'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('home'))
    expenses = user.my_expenses().all()
    # expenses = [
    #         {'owner' : owner, 'description' : 'Testing desc 1' },
    #         {'owner' : owner, 'description' : 'Testing desc 2' }
    #         ]
    return render_template('owner.html',
            user = user,
            expenses = expenses)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

from market import app
from flask import render_template , redirect , url_for , flash ,request
from market.models import Item ,User
from .forms import RegistrationForm, LoginForm ,PurshaseForm
from market import db 
# from market import login_manager
from flask_login import login_user , logout_user , login_required  , current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
@app.route('/market', methods=['POST','GET'])
@login_required
def market_page():
    purchase_form = PurshaseForm()
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None).all()
        return render_template('market.html', items=items , purchase_form=purchase_form)
    if request.method == 'POST':
        purshased_item = request.form.get('item_name')
        item_object = Item.query.filter_by(name=purshased_item).first()
        if item_object:
            if current_user.can_purshase(item_object):
                item_object.buy(current_user)
                flash(f"success! you Have bought:{item_object.name}", category="success")
            else:
                flash(f"Failed! You Don't have enogph budgets to Buy {item_object.name}", category="danger")
        return redirect(url_for('market_page'))

@app.route('/register', methods=['POST','GET'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_create = User(username=form.username.data,email=form.email.data,password=form.password1.data)
        db.session.add(user_create)
        db.session.commit()
        login_user(user_create)
        flash(f"success! you are logged in as :{user_create.username}", category="success")
        return redirect(url_for('market_page'))
    if form.errors !={}:    
        for form_err in form.errors.values():
            flash(f"there was an error creating the form:{form_err[0]}",category="danger")

    return render_template('register.html',form=form)

@app.route('/login', methods=['POST','Get'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(user_attempted_password=form.password.data) :
            login_user(attempted_user)
            flash(f"success! you are logged in as :{attempted_user.username}", category="success")
            return redirect(url_for('market_page'))
        else:
            flash('Username or Password Is not Correct',category="danger")


    if form.errors !={}:    
        for form_err in form.errors.values():
            flash(f"there was an error creating the form:{form_err[0]}",category="danger")
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You Have logged out!",category="info")
    return redirect('/home')

@app.route('/purshase' , methods=['GET'])
@login_required
def purshase_page():
    if request.method =="GET":
        items = Item.query.filter_by(owner=current_user.id).all()
        return render_template('purshase.html', items=items)




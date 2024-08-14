from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

connect_db(app)

#with app.app_context():
#    db.drop_all()
#    db.create_all()

@app.route('/')
def home():
    """Redirects to /register if not logged in"""
    with app.app_context():
        #if user logged in
        if "username" in session:
            return redirect(f"/users/{session['username']}")
        #user is not logged in
        else:
            return redirect('/register')
@app.route('/register', methods=['POST', 'GET'])
def show_register():
    """Show a form that when submitted will register/create a user"""
    with app.app_context():
        #ADD IF USER IS LOGGED IN
        form = RegisterForm()
        #if POST
        if form.validate_on_submit():
            #grabs data from form and creates new user
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
                
        #creates user instance 
            new_user = User.register(username, password, email, first_name, last_name)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect(f'/users/{new_user.username}')

        #if GET
        return render_template('register-form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        #if user is logged in, send them to their user page
        if "username" in session:
            return redirect(f"/users/{session['username']}")
        form = LoginForm()
        #if POST
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            
            user = User.authenticate(username, password)

            #if sucessfully logs in
            if user:
                session['username'] = user.username
                return redirect(f'/users/{username}')
            #doesn't log in
            else:
                form.username.errors = ["Invalid username/password."]
                return render_template("login-form.html", form=form)
        #if GET
        return render_template('login-form.html', form=form)
            
                 

@app.route('/users/<username>')
def show_user_page(username):
    with app.app_context():
        #if user is not logged in, or tries to access someone else's user page
        if "username" not in session or username != session['username']:
            raise Unauthorized()
        user = User.query.get_or_404(username)
        form = DeleteForm()

        return render_template('user-page.html', user=user, form=form)
        
@app.route('/logout')
def logout():
    """clears session and redirects to /"""
    with app.app_context():
        session.pop('username')
        return redirect('/login')
    


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

     #if user is not logged in, or tries to access someone else's user page
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
    with app.app_context():
        #Have to be logged in for this
        if "username" not in session or username != session['username']:
            raise Unauthorized()
        form = FeedbackForm()

        #if POST
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            #create new feedback instance
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{session['username']}")
        #if GET
        return render_template('feedback-form.html', form=form, username=username)
        
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    with app.app_context():
        #ADD checks that user is owner of this feedback
        feedback = Feedback.query.get_or_404(feedback_id)
        
        #if user is not logged in, or tries to access someone else's user page
        if "username" not in session or feedback.username != session['username']:
            raise Unauthorized()
        form = FeedbackForm(obj=feedback)

        #if POST
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f"/users/{session['username']}")

        #if GET
        return render_template('update-feedback-form.html', form=form, feedback=feedback)
        
@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    with app.app_context():
        """Delete feedback."""
    feedback = Feedback.query.get(feedback_id)
    if feedback.username != session['username']:
        raise Unauthorized()
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
        
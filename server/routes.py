from flask_wtf import FlaskForm
from server.storage.sessions import UserSession
from server.view.pages import PageFlash, PageRedirect, Request, PageRequest, PageUrlFor
from server.view.forms import RegistrationForm, LoginForm
from server.view.posts import BlogPost
from server.view.templates import BlogTemplatePosts, BlogTemplate
from server.storage.models import User
from server import blog, bcrypt, db
from flask_login import login_required
from server.view.users import CurrentUser


@blog.route('/')
@blog.route('/home')
def home() -> str:
    return BlogTemplatePosts('home.html').render(BlogPost())


@blog.route('/about')
def about() -> str:
    return BlogTemplate('about.html').render(title='About')


@blog.route('/register', methods=['GET', 'POST'])
def register() -> str:
    if CurrentUser().authenticated():
        return PageRedirect(PageUrlFor('home')).link()
    form: FlaskForm = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass: str = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user: User = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        UserSession(db).add(user)
        PageFlash(f'Your account has been created!'
                  f' You are now able to login with {user.username} username', 'success').display()
        return PageRedirect(PageUrlFor('login')).link()
    return BlogTemplate('register.html').render(title='Register', form=form)


@blog.route('/login', methods=['GET', 'POST'])
def login() -> str:
    if CurrentUser().authenticated():
        return PageRedirect(PageUrlFor('home')).link()
    form: FlaskForm = LoginForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            CurrentUser().login(user, form)
            next_page: Request = PageRequest('next').get()
            return PageRedirect(PageUrlFor(next_page if next_page else 'home')).link()
        else:
            PageFlash('Login Unsuccessful. Please check email and password', 'danger').display()
    return BlogTemplate('login.html').render(title='Login', form=form)


@blog.route('/logout')
def logout() -> str:
    CurrentUser().logout()
    return PageRedirect(PageUrlFor('home')).link()


@blog.route('/account')
@login_required
def account() -> str:
    return BlogTemplate('account.html').render(title='account')

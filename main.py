from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect, url_for, request, flash, abort
import random
from datetime import date
from forms import ContactForm, RegisterForm, LoginForm, CreateProjectPost
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup
from send_mail import Email
from flask_ckeditor import CKEditor
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
Bootstrap5(app)

# Authenticating/protecting the routes
login_manager = LoginManager()
login_manager.init_app(app)

# ADMIN ACCESS DECORATOR
def admin_access(func):
    @wraps(func)  # This fixes the endpoint naming issue, ensures that the original route is used
    def decorator_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403) # 👈 unauthenticated users

        if current_user.id != 1:
            abort(403)  # 👈 authenticated but not admin
        # if admin_id, it should process
        return func(*args, **kwargs)
    return decorator_function


# Tell Flask-CKEditor to use your custom CKEditor folder
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'custom'
app.config['CKEDITOR_CUSTOM_JS'] = 'ckeditor/ckeditor.js'

ckeditor = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class ProjectPosts(db.Model):
    __tablename__ = "project_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __init__(self, title, subtitle, body, img_url, date):
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.img_url = img_url
        self.date = date

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

with app.app_context():
    db.create_all()


# Providing a user_loader callback.
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


badge_classes = [
        "text-bg-primary",
        "text-bg-warning",
        "text-bg-secondary",
        "text-bg-success",
        "text-bg-info",
        "text-bg-dark",
        "text-bg-light"
    ]

python_labels = [
        "Data Analysis/Science: Pandas, NumPy, Scikit-Learn, SciPy",
        "Web Scraping: Selenium, Beautiful Soup",
        "Web Development: Flask & Jinja",
        "Databases: SQLite, SQLAlchemy, PostgreSQL",
        "Web Technologies: HTML, CSS & Bootstrap",
        "APIs: RESTful, JSON & requests library",
        "Visualizations: Matplotlib, Seaborn"
    ]

pbi_labels = [
    "Extract, Transform & Load",
    "Power Query",
    "Data Analysis Expression (DAX)",
    "Data Modeling",
    "Visualization & Design",
    "Communication and Reporting"
]

sql_labels = [
    "Data Querying",
    "Database Design",
    "Pivot tables",
    "Communication",
    "Collaboration"
]


@app.route("/")
def home():
    # Making a dictionary list of badges to display the skills randomly

    random.shuffle(badge_classes)  # Randomize badge order
    random.shuffle(python_labels)
    random.shuffle(pbi_labels)
    random.shuffle(sql_labels)

    # Pair each label with a class
    python_badges = [{"label": label, "class": cls} for label, cls in zip(python_labels, badge_classes)]
    pbi_badges = [{"label": label, "class": cls} for label, cls in zip(pbi_labels, badge_classes)]
    sql_badges = [{"label": label, "class": cls} for label, cls in zip(sql_labels, badge_classes)]

    # Randomizing the list of projects
    # projects = range(6)
    all_projects = db.session.execute(db.select(ProjectPosts)).scalars().all()
    random.shuffle(all_projects)   #This will randomize the projects list
    to_display = all_projects[:3]

    return render_template("index.html", projects=to_display, python_badges=python_badges,
                           pbi_badges=pbi_badges, sql_badges=sql_badges, logged_in=current_user.is_authenticated)


@app.route("/resume")
def resume():
    return render_template("resume.html", logged_in=current_user.is_authenticated)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form["name"].data
        email = contact_form["email"].data
        phone = contact_form["phone"].data
        message = contact_form["message"].data

        send_message = Email()

        try:
            send_message.post_email(name=name, email=email, phone=phone, message=message)
            flash("Successfully sent your message!", "success")
        except Exception as e:
            app.logger.error(f"Email failed: {e}")
            flash("Message sent, but email delivery failed.", "warning")

        return redirect(url_for("contact"))

    return render_template("contact.html", form=contact_form, logged_in=current_user.is_authenticated)

    # Clear the form field without redirecting which is the cleanest way to clear the form but resubmits on refreshing
    # contact_form.process(formdata=None)


@app.route("/create-project", methods=["GET", "POST"])
@admin_access
def create_project():
    project_post = CreateProjectPost()
    if project_post.validate_on_submit():
        new_project = ProjectPosts(
            title=project_post.title.data,
            subtitle=project_post.subtitle.data,
            body=project_post.body.data,
            img_url=project_post.img_url.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("projects")) #change it to projects
    return render_template("create_project.html", form=project_post, logged_in=current_user.is_authenticated)


@app.route("/edit-project<int:project_id>", methods=["GET", "POST"])
@admin_access
def edit_project(project_id):
    # get the current user_id of the user and check if it has an id==1
    project = db.get_or_404(ProjectPosts, project_id)
    edit_form = CreateProjectPost(
        title=project.title,
        subtitle=project.subtitle,
        img_url=project.img_url,
        body=project.body
    )
    if edit_form.validate_on_submit():
        project.title = edit_form.title.data
        project.subtitle = edit_form.subtitle.data
        project.img_url = edit_form.img_url.data
        project.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_project", project_id=project.id, logged_in=current_user.is_authenticated))

    return render_template("create_project.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated)


@app.route("/projects")
def projects():
    page = request.args.get("page", 1, type=int)
    per_page = 5  # number of projects per page

    pagination = db.paginate(
        db.select(ProjectPosts).order_by(ProjectPosts.id.desc()),
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "all_projects.html",
        all_projects=pagination.items,
        pagination=pagination,
        logged_in=current_user.is_authenticated
    )


@app.route("/project/<int:project_id>")
def show_project(project_id):
    requested_project = db.get_or_404(ProjectPosts, project_id)
    return render_template("show_project.html", project=requested_project, logged_in=current_user.is_authenticated)


@app.route("/delete/<int:project_id>", methods=["GET", "POST"])
@admin_access
def delete(project_id):
    project = db.get_or_404(ProjectPosts, project_id)
    
    if request.method == "POST":
        db.session.delete(project)
        db.session.commit()
        flash("Project deleted successfully.")
        return redirect(url_for("projects"))

    # GET request → show confirmation page
    return render_template("confirm_delete.html", project=project)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Hide the registration route entirely if user exists
    if db.session.execute(db.select(User).limit(1)).scalar_one_or_none():
        abort(403)

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        password = register_form.password.data
        email = register_form.email.data
        name = register_form.name.data

        hashed_password = generate_password_hash(password, method='scrypt', salt_length=10)

        # Inputting the form parameters and the hashed password and saving in the User db
        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
            
        flash("Thanks for registering!", "success")
        login_user(user)
        return redirect(url_for('home'))

    return render_template("register.html", form=register_form, logged_in=current_user.is_authenticated)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            flash(Markup(f"This email does not exist. Please try again!"))
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect. Please try again!")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=login_form, logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/test')
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
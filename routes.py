import os
import json
import re
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from apiRequest import Request
from apiRequest import Article
from apiRequest import Article_Encoder


baseRequest = "https://newsapi.org/v2/"
string_api_key = "apiKey=" + os.environ.get('API_KEY')
apiKey = string_api_key
everythingOrTop = "everything?"
category = ""
sortBy = "sortBy=popularity"
q = ""

load_dotenv()
app = Flask(__name__, static_folder = 'static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('DATABASE_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    preferences = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"User: {self.email}"

db.init_app(app)
with app.app_context():
    # User.__table__.drop(db.engine)
    db.create_all()

# ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # form = LoginForm(request.form)
        email = request.form["email"]
        password = request.form["password"]

        if not email or not password:
            return jsonify({'message': 'Invalid input'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            error = "Invalid email or password"
            return render_template("login.html", error = error)

        if not pbkdf2_sha256.verify(password, user.password):
            error = "Invalid email or password"
            return render_template("login.html", error = error, email = email, password = password)

        session["email"] = user.email

        return redirect(url_for("myfive"))
        # return jsonify({'message': 'Login successful'}), 200
    else:
        if "email" in session:
            return render_template("myfive.html")
        print(request.referrer)
        came_from = request.referrer
        return render_template("login.html", came_from = came_from)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        preferences = request.form.getlist("preferences")

        if not email or not password:
            warning = "Email or password cannot be empty"
            return render_template("signup.html", warning = warning)
        elif not preferences:
            warning = "You must select at least 1 preference."
            return render_template("signup.html", pref_warning = warning)
        
        valid = data_check(password)

        if not valid:
            password_warning = "Passwords must contain at least 1 uppercase, 1 lowercase, 1 digit, 1 special character and be at least 6 characters in length"
            return render_template("signup.html", password_warning = password_warning, email = email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = pbkdf2_sha256.hash(password)

        string_preferences = json.dumps(preferences)

        new_user = User(email=email, password=hashed_password, preferences = string_preferences)
        db.session.add(new_user)
        db.session.commit()

        session["email"] = new_user.email

        return redirect(url_for("myfive"))
        # return jsonify({'message': 'User created successfully'}), 201
    else:
        return render_template("signup.html")
    
def data_check(password):
    password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=!]).{8,}$"

    password_match = re.search(password_pattern, password)

    if password_match:
        return True
    else:
        return False


@app.route("/environment")
def environ():
    if "email" in session:
        if "environ_articles" in session:
            articles2 = json.loads(session["environ_articles"])
            return render_template("environment.html", articles = articles2)
        else: 
            request = Request()
            final_request = request.select_category("environment", baseRequest, apiKey, everythingOrTop)
            unsigned_articles = request.api_request(final_request)

            decoded_articles = request.decode_url(unsigned_articles)
            cleaned_articles = request.clean_article_data(decoded_articles)
            articles_list = request.query_article_data(cleaned_articles)


            article_objects_list = []

            for i in articles_list:
                article = Article(i[0], i[1], i[2])
                article_objects_list.append(article)

            json_articles = json.dumps(article_objects_list, indent=4, cls=Article_Encoder)
            session["environ_articles"] = json_articles

            return render_template("environment.html", articles = article_objects_list)
    else:      
        return redirect(url_for("login"))

@app.route("/politics")
def politics():
    if "email" in session:
        if "politic_articles" in session:
            articles2 = json.loads(session["politic_articles"])
            return render_template("politics.html", articles = articles2)
        else:        
            request = Request()
            final_request = request.select_category("politics", baseRequest, apiKey, everythingOrTop)
            unsigned_articles = request.api_request(final_request)

            decoded_articles = request.decode_url(unsigned_articles)
            cleaned_articles = request.clean_article_data(decoded_articles)
            articles_list = request.query_article_data(cleaned_articles)


            article_objects_list = []

            for i in articles_list:
                article = Article(i[0], i[1], i[2])
                article_objects_list.append(article)

            json_articles = json.dumps(article_objects_list, indent=4, cls=Article_Encoder)
            session["politic_articles"] = json_articles

        return render_template("politics.html", articles = article_objects_list)
    else:      
        return redirect(url_for("login"))

@app.route("/general")
def genreral():
    if "email" in session:
        if "general_articles" in session:
            articles2 = json.loads(session["general_articles"])
            return render_template("general.html", articles = articles2)
        else:
            request = Request()
            final_request = request.select_category("general", baseRequest, apiKey, everythingOrTop)
            unsigned_articles = request.api_request(final_request)

            decoded_articles = request.decode_url(unsigned_articles)
            cleaned_articles = request.clean_article_data(decoded_articles)
            articles_list = request.query_article_data(cleaned_articles)


            article_objects_list = []

            for i in articles_list:
                article = Article(i[0], i[1], i[2])
                article_objects_list.append(article)

            json_articles = json.dumps(article_objects_list, indent=4, cls=Article_Encoder)
            session["general_articles"] = json_articles

            return render_template("general.html", articles = article_objects_list)
    else:      
        return redirect(url_for("login"))

@app.route("/sports")
def sports():
    if "email" in session:
        if "sport_articles" in session:
            articles2 = json.loads(session["sport_articles"])
            return render_template("sports.html", articles = articles2)
        else: 
            request = Request()
            final_request = request.select_category("sports", baseRequest, apiKey, everythingOrTop)
            unsigned_articles = request.api_request(final_request)

            decoded_articles = request.decode_url(unsigned_articles)
            cleaned_articles = request.clean_article_data(decoded_articles)
            articles_list = request.query_article_data(cleaned_articles)


            article_objects_list = []

            for i in articles_list:
                article = Article(i[0], i[1], i[2])
                article_objects_list.append(article)

            json_articles = json.dumps(article_objects_list, indent=4, cls=Article_Encoder)
            session["sport_articles"] = json_articles
            
            return render_template("sports.html", articles = article_objects_list)
    else:      
        return redirect(url_for("login"))

@app.route("/technology")
def tech():
    if "email" in session:
        if "tech_articles" in session:
            articles2 = json.loads(session["tech_articles"])
            return render_template("technology.html", articles = articles2)
        else: 
            request = Request()
            final_request = request.select_category("technology", baseRequest, apiKey, everythingOrTop)
            unsigned_articles = request.api_request(final_request)

            decoded_articles = request.decode_url(unsigned_articles)
            cleaned_articles = request.clean_article_data(decoded_articles)
            articles_list = request.query_article_data(cleaned_articles)


            article_objects_list = []

            for i in articles_list:
                article = Article(i[0], i[1], i[2])
                article_objects_list.append(article)

            json_articles = json.dumps(article_objects_list, indent=4, cls=Article_Encoder)
            session["tech_articles"] = json_articles

            return render_template("technology.html", articles = article_objects_list)
    else:      
        return redirect(url_for("login"))

@app.route("/myfive")
def myfive():
    if "email" in session:
        return render_template("myfive.html")
    else:      
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("environ_articles", None)
    session.pop("tech_articles", None)
    session.pop("sport_articles", None)
    session.pop("general_articles", None)
    session.pop("politic_articles", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug = True)
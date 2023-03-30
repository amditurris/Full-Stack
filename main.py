from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()
OWN_EMAIL = "youremail@gmail.com"
OWN_PASSWORD = "youpassword"
GMAIL_SMTP_SERVER = "smtp.gmail.com"


app = Flask(__name__)


@app.route('/')
def homepage():
    blog_url = "https://api.npoint.io/5ff5f2c4a307820c3ae5"
    response_blog = requests.get(blog_url)
    all_post = response_blog.json()
    return render_template('index.html', posts=all_post)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == "POST":
        data = request.form
        name = (data["username"])
        email = (data["useremail"])
        phone = (data["userphone"])
        message = (data["usertext"])

        email_message = f'''Subject:New Message\n
            Name: {name}\n
            Email: {email}\n
            Phone: {phone}\n
            Message: {message}'''
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(GMAIL_SMTP_SERVER, OWN_EMAIL, email_message)

        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


@app.route('/post<num>')
def only_post(num):
    number = int(num) - 1
    blog_url = "https://api.npoint.io/5ff5f2c4a307820c3ae5"
    response_blog = requests.get(blog_url)
    all_post = response_blog.json()
    the_post = all_post[number]
    return render_template("post.html", posted=the_post)


# @app.route('/form-entry', methods=['GET', 'POST'])
# def receive_data():
#     name = request.form['username']
#     email = request.form['useremail']
#     phone = request.form['userphone']
#     text = request.form['usertext']
#     return f"<p>Name: {name}, Email: {email}, Phone: {phone}, Message: {text}</p>"


if __name__ == '__main__':
    app.run(debug=True)
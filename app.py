from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///compliments.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Отключение кэширования
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    last_compliment_date = db.Column(db.Date, nullable=True)
    compliments_used = db.Column(db.Text, default="")
    last_image_used = db.Column(db.String(200), nullable=True)


class Compliment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)


def initialize_database():
    with app.app_context():
        db.create_all()
        compliments = [
            "Ты самая заботливая мама на свете!",
            "Ты умеешь сделать мир ярче своим присутствием!",
            "Твоя забота о близких безгранична.",
            "Ты — источник вдохновения для многих!",
            "Ты самый добрый человек, которого я знаю!",
            "Ты всегда в центре внимания, потому что ты особенная.",
            "Каждый день с тобой — это праздник.",
            "Ты невероятно красива внутри и снаружи!",
            "Ты — мой самый верный друг и поддержка.",
            "Ты — волшебница, делающая мир лучше.",
            "С Днем Матери! Ты — волшебница, которая делает этот мир лучше!"
        ]
        existing_texts = {c.text for c in Compliment.query.all()}
        for c in compliments:
            if c not in existing_texts:
                db.session.add(Compliment(text=c))
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if not User.query.filter_by(email=email).first():
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('card', email=email))
    return render_template('index.html')


@app.route('/card/<email>')
def card(email):
    user = User.query.filter_by(email=email).first()
    today = datetime.date.today()

    if not user:
        return redirect(url_for('index'))

    print("Today's date:", today)
    print("User's last compliment date:", user.last_compliment_date)
    print("User's compliments used:", user.compliments_used)
    print("User's last image used:", user.last_image_used)

    if today == datetime.date(2024, 11, 24):
        special_compliment = Compliment.query.filter_by(
            text="С Днем Матери! Ты — волшебница, которая делает этот мир лучше!").first()
        compliment = special_compliment.text
        image_path = "special_image.jpg"
        user.last_image_used = image_path
        db.session.commit()
    else:
        if user.last_compliment_date == today and user.compliments_used:
            last_compliment_id = int(user.compliments_used.split(",")[-1])
            compliment = Compliment.query.get(last_compliment_id).text
        else:
            all_compliments = Compliment.query.all()
            used_ids = [int(i) for i in user.compliments_used.split(",") if i]
            available_compliments = [c for c in all_compliments if c.id not in used_ids]
            if not available_compliments:
                available_compliments = all_compliments
            compliment_obj = random.choice(available_compliments)

            user.last_compliment_date = today
            used_ids.append(compliment_obj.id)
            user.compliments_used = ",".join(map(str, used_ids))
            compliment = compliment_obj.text

            image_path = random.choice(["image1.jpg", "image2.jpg", "image3.jpg"])
            user.last_image_used = image_path
            db.session.commit()

    if not user.last_image_used:
        user.last_image_used = "default_image.jpg"
        db.session.commit()

    print("Images in static/images:", os.listdir('static/images'))
    return render_template('card.html', compliment=compliment, user=user, today=today)


@app.route('/memories/<email>', methods=['GET', 'POST'])
def memories(email):
    if request.method == 'POST':
        return jsonify({"status": "success"})
    return render_template('memories.html')


if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000)

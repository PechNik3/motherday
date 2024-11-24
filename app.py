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
            "Мама, ты всегда была для меня не только мамой, но и самым близким человеком, которому я могу доверить любые мысли и чувства. Твоя любовь окружает меня, как невидимый щит, и даёт мне уверенность в том, что я могу справиться с любыми трудностями. Ты всегда знаешь, как поддержать меня в нужный момент, и даже твоя простая улыбка способна развеять все мои тревоги. Спасибо за твою мудрость, терпение и за то, что всегда веришь в меня даже тогда, когда я сомневаюсь в себе.",
            "Каждый день я всё больше понимаю, каким счастьем для меня было расти рядом с тобой. Ты научила меня ценить добро, уважать других людей и видеть красоту в простых вещах. Когда я был маленьким, я думал, что это просто твоя обязанность — заботиться обо мне. Но с годами я понял, сколько усилий ты вкладывала, чтобы сделать моё детство светлым и счастливым. Твоя любовь и поддержка стали фундаментом, на котором строится вся моя жизнь. Я горжусь тем, что у меня есть такая мама.",
            "Мама, ты мой лучший друг и самый преданный союзник. Ты никогда не отворачивалась от меня, даже в те моменты, когда я ошибался. Вместо осуждения я всегда находил у тебя понимание и поддержку. Ты умеешь находить правильные слова, которые вдохновляют и подбадривают, а твоя вера в меня заставляет верить в самого себя. Без тебя я бы не стал тем человеком, которым являюсь сегодня. Я бесконечно благодарен тебе за всё, что ты сделала и продолжаешь делать для меня.",
            "Мама, ты для меня — настоящее чудо. Я всё больше осознаю, насколько ты сильный и невероятно добрый человек. Твоя способность справляться с трудностями и сохранять тепло в сердце — это что-то, чему я всегда хочу у тебя учиться. Ты делаешь наш дом местом, куда хочется возвращаться снова и снова, где я чувствую себя в полной безопасности. Ты не просто мама, ты — мой пример того, каким человеком стоит быть: честным, искренним, заботливым. Я горжусь тобой и тем, что могу называть тебя своей мамой.",
            "Мама, иногда мне сложно выразить словами, как сильно я тебя люблю и как много ты для меня значишь. Ты дала мне не только жизнь, но и всё, что нужно, чтобы быть счастливым. Ты всегда была рядом — и в радостные, и в трудные моменты, обнимая меня своим теплом и мудрыми словами. Твоя вера в мои силы — это тот свет, который ведёт меня вперёд даже в самых сложных ситуациях. Спасибо за твои жертвы, за твоё терпение, за ту любовь, которая никогда не угасает. Ты — мой герой, мой ангел-хранитель, моя самая родная мама.",
        ]
        # compliments = [
        #     "Мама, ты для меня — источник любви и вдохновения. Без тебя я бы не стал тем, кто я есть.",
        #     "Каждое твое слово наполняет мою жизнь теплом. Ты — мое главное богатство.",
        #     "Мама, твоя забота и поддержка сделали мою жизнь невероятно счастливой. Спасибо тебе за это.",
        #     "Твоя улыбка для меня — самый красивый свет в мире. Ты делаешь каждый мой день лучше.",
        #     "Ты умеешь любить всем сердцем, и я чувствую это каждую минуту. Спасибо за твою безграничную доброту.",
        #     "Ты всегда находишь правильные слова, чтобы поддержать меня. Ты — мой главный наставник и друг.",
        #     "Мама, с тобой я знаю, что мне всё по силам. Твоя вера в меня — моя главная сила.",
        #     "Ты делаешь дом самым уютным местом на земле. С тобой так тепло и спокойно.",
        #     "Мама, я восхищаюсь твоей мудростью. Ты всегда знаешь, как поступить правильно.",
        #     "Ты умеешь превращать обыденное в волшебство. Каждый момент с тобой — это праздник.",
        #     "Ты — мой лучший друг, которому я могу доверить всё. Спасибо за твою искренность.",
        #     "Мама, ты моя героиня. Ты справляешься с такими трудностями, что мне есть чему у тебя учиться.",
        #     "Ты всегда была для меня примером силы и доброты. Я горжусь тем, что ты моя мама.",
        #     "Мама, ты — мой путеводный свет. Без тебя я бы никогда не нашёл свой путь.",
        #     "Ты учишь меня видеть добро в людях. С тобой я становлюсь лучше каждый день.",
        #     "Ты умеешь любить так, как никто другой. Твоя любовь для меня дороже всего.",
        #     "Мама, ты делаешь этот мир добрее. Я горжусь тем, что могу называть тебя своей мамой.",
        #     "Ты не только моя мама, но и мой лучший друг. Я благодарен за то, что ты всегда рядом.",
        #     "Ты всегда веришь в меня, даже когда я сомневаюсь в себе. Спасибо за твою поддержку.",
        #     "Мама, твоя сила и нежность — это то, что делает тебя уникальной. Я тобой восхищаюсь.",
        #     "Ты наполнила мою жизнь любовью, которая остаётся со мной в каждом моменте.",
        #     "Мама, ты всегда заботилась обо мне, даже тогда, когда я этого не замечал. Спасибо за всё.",
        #     "С тобой я чувствую себя защищённым и любимым. Ты — мой самый родной человек.",
        #     "Ты научила меня не сдаваться и верить в лучшее. Спасибо за это, мама.",
        #     "Ты делаешь каждый день особенным, просто будучи рядом. Я тебя очень люблю.",
        #     "Мама, ты мой источник вдохновения. Я хочу быть таким же добрым и сильным, как ты.",
        #     "Ты всегда ставишь меня на первое место. Спасибо за твою любовь и заботу.",
        #     "Мама, ты как лучик солнца, который освещает мою жизнь. Ты для меня всё.",
        #     "С Днем Матери! Ты — моя опора, вдохновение и самая лучшая мама в мире."
        # ]

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
            text="Мама, ты мой лучший друг и самый преданный союзник. Ты никогда не отворачивалась от меня, даже в те моменты, когда я ошибался. Вместо осуждения я всегда находил у тебя понимание и поддержку. Ты умеешь находить правильные слова, которые вдохновляют и подбадривают, а твоя вера в меня заставляет верить в самого себя. Без тебя я бы не стал тем человеком, которым являюсь сегодня. Я бесконечно благодарен тебе за всё, что ты сделала и продолжаешь делать для меня.",
            ).first()
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

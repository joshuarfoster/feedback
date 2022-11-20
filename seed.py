from models import User, Feedback, db
from app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

with app.app_context():


    db.drop_all()
    db.create_all()

    Jerryhashed = bcrypt.generate_password_hash('tadpole123')
    Jerrypwd = Jerryhashed.decode("utf8")
    Jerry = User(username='jerrylovesfrogs',password=Jerrypwd,email='frogman@gmail.com',first_name='Jerry',last_name='Jones')
    Kimhashed = bcrypt.generate_password_hash('ronstoppable')
    Kimpwd = Kimhashed.decode("utf8")
    Kim = User(username='kimpossible',password=Kimpwd,email='kimdoesntstop@gmail.com',first_name='Kim',last_name='Smith')
    Rickhashed = bcrypt.generate_password_hash('12345')
    Rickpwd = Rickhashed.decode("utf8")
    Rick = User(username='Rickster',password=Rickpwd,email='Rickster123@gmail.com',first_name='Rick',last_name='Rodger')
    Susanhashed = bcrypt.generate_password_hash('equestrian24')
    Susanpwd = Susanhashed.decode("utf8")
    Susan = User(username='Horselover',password=Susanpwd,email='stablegirl@gmail.com',first_name='Susan',last_name='Long')

    db.session.add(Jerry)
    db.session.add(Kim)
    db.session.add(Rick)
    db.session.add(Susan)

    db.session.commit()

    JerryFeedback = Feedback(title='Displeased', content='Not pleased with service', username='jerrylovesfrogs')
    KimFeedback = Feedback(title='Displeased', content='Not pleased with service', username='kimpossible')
    RickFeedback = Feedback(title='Displeased', content='Not pleased with service', username='Rickster')
    SusanFeedback = Feedback(title='Displeased', content='Not pleased with service', username='Horselover')

    db.session.add(JerryFeedback)
    db.session.add(KimFeedback)
    db.session.add(RickFeedback)
    db.session.add(SusanFeedback)

    db.session.commit()
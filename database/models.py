from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Training(db.Document):
    language = db.StringField(required=True)
    data = db.DictField(required=True)

class CustomPalette(db.Document):
    title = db.StringField(required=True)
    colors = db.DictField(required=True)
    author = db.ReferenceField('User')

class CustomCard(db.Document):
    text = db.StringField(required=True)
    pos = db.StringField(required=True)
    image = db.StringField(required=True)
    custom_color = db.StringField()
    card_meta = db.DictField(required=True)
    author = db.ReferenceField('User')

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    custom_cards = db.ListField(db.ReferenceField('CustomCard', reverse_delete_rule=db.PULL))
    custom_palettes = db.ListField(db.ReferenceField('CustomPalette', reverse_delete_rule=db.PULL))
    settings = db.DictField(required=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(CustomCard, 'author', db.CASCADE)
User.register_delete_rule(CustomPalette, 'author', db.CASCADE)

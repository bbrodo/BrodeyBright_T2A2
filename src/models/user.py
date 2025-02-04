from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp


class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    groups = db.relationship('Group', back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    songs = db.relationship("Song", back_populates="user")


class UserSchema(ma.Schema):
    groups = fields.List(fields.Nested('GroupSchema', exclude=["user"]))
    comments = fields.List(fields.Nested('CommentSchema', exclude=["user"]))
    songs = fields.List(fields.Nested('SongSchema', exclude=["user"]))

    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format"))

    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Minimum eight characters, at least one letter and one number"))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "groups", "songs", "comments")


# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])
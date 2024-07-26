from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_TYPES = ( "Album", "Single", "EP", "LP" )

class Group(db.Model):
    # name of the table
    __tablename__ = "groups"
    # attributes of the table

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.Date) # Created Date
    type = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='groups')
    comments = db.relationship("Comment", back_populates="group", cascade="all, delete")
    songs = db.relationship("Song", back_populates="group", cascade="all, delete")



class GroupSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    comments = fields.List(fields.Nested("CommentSchema", exclude=["group"]))
    songs = fields.List(fields.Nested("SongSchema", exclude=["group"]))

    title = fields.String(required=True, validate=And(
        Length(min=1, error="Title must be at least 1 characters long")
    ))

    type = fields.String(validate=OneOf(VALID_TYPES))


    class Meta:
        fields = ( "id", "title", "description", "date", "type", "user", "songs", "comments" )
        ordered = True


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
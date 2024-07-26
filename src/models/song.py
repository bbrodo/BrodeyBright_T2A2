from init import db, ma
from marshmallow import fields

class Song(db.Model):
    # name of the table
    __tablename__ = "songs"
    # attributes of the table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

    user = db.relationship("User", back_populates="songs")
    group = db.relationship("Group", back_populates="songs")


class SongSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    group = fields.Nested("GroupSchema", exclude=["songs"])

    class Meta:
        fields = ("id", "name", "user", "group")


song_schema = SongSchema()
songs_schema = SongSchema(many=True)
from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    # name of the table
    __tablename__ = "comments"
    # attributes of the table

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.Date) # Created Date

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

    user = db.relationship("User", back_populates="comments")
    group = db.relationship("Group", back_populates="comments")


class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    group = fields.Nested("GroupSchema", exclude=["comments"])

    class Meta:
        fields = ("id", "message", "date", "user", "group")


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
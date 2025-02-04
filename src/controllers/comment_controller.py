from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.group import Group

# /cards/<int:group_id>/comments
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:group_id>/comments")

# we already get the comments while fetching cards, so, no need for "get comments" route here

# Create comment route
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(group_id):
    # get the comment object from the request body
    body_data = request.get_json()
    # fetch the group with that particular id - group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # if group exists
    if group:
        # create an instance of the Comment model
        comment = Comment(
            message=body_data.get("message"),
            date=date.today(),
            group=group,
            user_id=get_jwt_identity()
        )
        # add and commit the session
        db.session.add(comment)
        db.session.commit()
        # return the created commit
        return comment_schema.dump(comment), 201
    # else
    else:
        # return an error like group does not exist
        return {"error": f"Group with id {group_id} not found"}, 404

# Delete Comment - /cards/group_id/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(group_id, comment_id):
    # fetch the comment from the db with that id - comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # delete the comment
        db.session.delete(comment)
        db.session.commit()
        # return some message
        return {"message": f"Comment '{comment.message}' deleted successfully"}
    # else
    else:
        # return an error saying comment does not exist
        return {"error": f"Comment with id {comment_id} not found"}, 404


# Update comment - /cards/group_id/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_comment(group_id, comment_id):
    # get the values from the body of the request
    body_data = request.get_json()
    # find the comment from the db with the id - comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # update the fields
        comment.message = body_data.get("message") or comment.message
        # commit
        db.session.commit()
        # return some response to the client
        return comment_schema.dump(comment)
    # else
    else:
        # return error saying comment does not exist
        return {"error": f"Comment with id {comment_id} not found"}, 404
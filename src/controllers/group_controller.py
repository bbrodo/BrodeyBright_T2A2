from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.comment_controller import comments_bp
from controllers.song_controller import songs_bp
from utils import authorise_as_admin

from init import db
from models.group import Group, group_schema, groups_schema

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")
groups_bp.register_blueprint(comments_bp)
groups_bp.register_blueprint(songs_bp)

# /groups - GET - fetch all groups
# /groups/<id> - GET - fetch a single group
# /groups - POST - create a new group
# /groups/<id> - DELETE - delete a group
# /groups/<id> - PUT, PATCH - edit a group

# /groups - GET - fetch all groups
@groups_bp.route("/")
def get_all_groups():
    # fetch all groups and order them according to date in descending order
    stmt = db.select(Group).order_by(Group.date.desc())
    groups = db.session.scalars(stmt)
    return groups_schema.dump(groups)

# /groups/<id> - GET - fetch a single group
@groups_bp.route("/<int:group_id>")
def get_one_group(group_id):
    stmt = db.select(Group).filter_by(id=group_id)
    # stmt = db.select(group).where(group.id==group_id)
    group = db.session.scalar(stmt)
    if group:
        return group_schema.dump(group)
    else:
        return {"error": f"group with id {group_id} not found"}, 404


# /groups - POST - create a new group
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def create_group():
    # get the data from the body of the request
    body_data = group_schema.load(request.get_json())
    # create a new group model instance
    group = Group(
        title=body_data.get("title"),
        description=body_data.get("description"),
        date=date.today(),
        type=body_data.get("type"),
        user_id=get_jwt_identity()
    )
    # add and commit to DB
    db.session.add(group)
    db.session.commit()
    # respond
    return group_schema.dump(group)


# /groups/<id> - DELETE - delete a group
@groups_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group(group_id):
    # fetch the group from the database
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # if group
    if group:
                # check whether the user is an admin or not
        is_admin = authorise_as_admin()
        if not is_admin and str(group.user_id) != get_jwt_identity():
            return {"error": "User is not authorised to perform this action."}, 403
        # delete the group
        db.session.delete(group)
        db.session.commit()
        return {"message": f"group '{group.title}' deleted successfully"}
    # else
    else:
        # return error
        return {"error": f"group with id {group_id} not found"}, 404


# /groups/<id> - PUT, PATCH - edit a group
@groups_bp.route("/<int:group_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_group(group_id):
    # get the data from the body of the request
    body_data = group_schema.load(request.get_json(), partial=True)
    # get the group from the database
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # if group
    if group:
                
        # if the user is not the owner of the group
        if str(group.user_id) != get_jwt_identity():
            return {"error": "You are not the owner of the group"}, 403

        # update the fields as required
        group.title = body_data.get("title") or group.title
        group.description = body_data.get("description") or group.description
        group.type = body_data.get("type") or group.type
        # commit to the DB
        db.session.commit()
        # return a response
        return group_schema.dump(group)
    # else
    else:
        # return an error
        return {"error": f"group with id {group_id} not found"}, 404
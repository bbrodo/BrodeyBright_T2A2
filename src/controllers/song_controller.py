from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.song import Song, song_schema, songs_schema
from models.group import Group

# /cards/<int:group_id>/songs
songs_bp = Blueprint("songs", __name__, url_prefix="/<int:group_id>/songs")

# we already get the songs while fetching cards, so, no need for "get songs" route here

# Create song route
@songs_bp.route("/", methods=["POST"])
@jwt_required()
def create_song(group_id):
    # get the song object from the request body
    body_data = request.get_json()
    # fetch the group with that particular id - group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # if group exists
    if group:
        # create an instance of the song model
        song = Song(
            name=body_data.get("name"),
            group=group,
            user_id=get_jwt_identity()
        )
        # add and commit the session
        db.session.add(song)
        db.session.commit()
        # return the created commit
        return song_schema.dump(song), 201
    # else
    else:
        # return an error like group does not exist
        return {"error": f"Group with id {group_id} not found"}, 404

# Delete song - /cards/group_id/songs/song_id
@songs_bp.route("/<int:song_id>", methods=["DELETE"])
@jwt_required()
def delete_song(group_id, song_id):
    # fetch the song from the db with that id - song_id
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    # if song exists
    if song:
        # delete the song
        db.session.delete(song)
        db.session.commit()
        # return some name
        return {"name": f"song '{song.name}' deleted successfully"}
    # else
    else:
        # return an error saying song does not exist
        return {"error": f"song with id {song_id} not found"}, 404


# Update song - /cards/group_id/songs/song_id
@songs_bp.route("/<int:song_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_song(group_id, song_id):
    # get the values from the body of the request
    body_data = request.get_json()
    # find the song from the db with the id - song_id
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    # if song exists
    if song:
        # update the fields
        song.name = body_data.get("name") or song.name
        # commit
        db.session.commit()
        # return some response to the client
        return song_schema.dump(song)
    # else
    else:
        # return error saying song does not exist
        return {"error": f"song with id {song_id} not found"}, 404
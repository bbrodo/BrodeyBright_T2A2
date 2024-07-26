from flask import Blueprint
from datetime import date

from init import db, bcrypt
from models.user import User
from models.group import Group
from models.comment import Comment
from models.song import Song

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    # create a list of User instances
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
        )
    ]

    db.session.add_all(users)
    # create a list of group instances
    groups = [
        Group(
            title="Album 1",
            description="album 1 desc",
            date=date.today(),
            type="Album",
            user=users[0]
        ),
        Group(
            title="Single 1",
            description="single 1 desc",
            date=date.today(),
            type="Single",
            user=users[0]
        ),
        Group(
            title="Album 2",
            description="album 2 desc",
            date=date.today(),
            type="Album",
            user=users[1]
        )
    ]

    db.session.add_all(groups)
    # create a list of comment instances
    comments = [
        Comment(
            message="Comment 1",
            date=date.today(),
            user=users[1],
            group=groups[0]
        ),
        Comment(
            message="Comment 2",
            date=date.today(),
            user=users[0],
            group=groups[0]
        ),
        Comment(
            message="Comment 3",
            date=date.today(),
            user=users[0],
            group=groups[2]
        )
    ]

    db.session.add_all(comments)
    # create a list of song instances
    songs = [
        Song(
            name="Song 1",
            user=users[1],
            group=groups[0]
        ),
        Song(
            name="Song 2",
            user=users[0],
            group=groups[0]
        ),
        Song(
            name="Song 3",
            user=users[0],
            group=groups[2]
        )
    ]

    db.session.add_all(songs)

    db.session.commit()

    print("Tables seeded")
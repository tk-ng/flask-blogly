"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


default_img_url = "https://pngimg.com/uploads/simpsons/simpsons_PNG20.png"


class User(db.Model):
    """ User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=False,
                          default=default_img_url)

    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<User first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    @classmethod
    def delete_by_id(cls, user_id):
        """Delete the user by its id."""
        return cls.query.filter(cls.id == user_id).delete()

    @property
    def full_name(self):
        """return the full name."""
        return f"{self.first_name} {self.last_name}"

    # def get_full_name(self):
    #     """return the full name."""
    #     return f"{self.first_name} {self.last_name}"

    # full_name = property(
    #     fget=get_full_name
    # )

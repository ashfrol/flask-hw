from sqlalchemy import exc
from sqlalchemy.sql.coercions import cls

import errors
from app import db


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck

    def del_obj(self):
        db.session.delete(self)
        self.try_to_commit()

    @staticmethod
    def try_to_commit():
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class Ad(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    owner = db.Column(db.String(64))

    def __str__(self):
        return '<Title {}>'.format(self.title)

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner': self.owner
        }

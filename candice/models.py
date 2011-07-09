# coding: utf-8

# Candice, aplicación web agregando información sobre candidatos políticos.
# Copyright (C) 2011 Renzo Carbonara <renzo @carbonara punto com punto ar>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flaskext.sqlalchemy import SQLAlchemy
from candice import app

__all__ = 'db', 'Candidate', 'Party', 'Charge'


db = SQLAlchemy(app)


class _AddReprMixin(object):
    def __repr__(self):
        s = u'<%s.%s %s>' % (self.__class__.__module__,
                             self.__class__.__name__, unicode(self))
        return s.encode('utf-8')


class Candidate(db.Model, _AddReprMixin):
    __tableame__ = 'candidate'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(127), unique=True, nullable=False)
    name = db.Column(db.Unicode(127), nullable=False)
    email = db.Column(db.Unicode(127), nullable=False, default=u'')
    website = db.Column(db.Unicode(255), nullable=False, default=u'')
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    charge_id = db.Column(db.Integer, db.ForeignKey('charge.id'), nullable=False)

    def __unicode__(self):
        return unicode(self.name)


class Party(db.Model, _AddReprMixin):
    __tableame__ = 'party'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(127), unique=True, nullable=False)
    name = db.Column(db.Unicode(127), nullable=False)
    acronym = db.Column(db.Unicode(127), nullable=False, default=u'')
    website = db.Column(db.Unicode(255), nullable=False, default=u'')
    candidates = db.relationship('Candidate', lazy='dynamic', backref='party')

    def __unicode__(self):
        if self.acronym:
            return u'%s (%s)' % (self.name, self.acronym)
        return unicode(self.name)


class Charge(db.Model, _AddReprMixin):
    __tablename__ = 'charge'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(127), unique=True, nullable=False)
    province = db.Column(db.Unicode(127))
    department = db.Column(db.Unicode(127))
    locality = db.Column(db.Unicode(127))
    candidate = db.relationship('Candidate', lazy='dynamic', backref='charge')

    def __unicode__(self):
        return unicode(self.name)


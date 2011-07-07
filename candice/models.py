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


db = SQLAlchemy(app)


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(127), unique=True)
    name = db.Column(db.Unicode(127))
    email = db.Column(db.Unicode(127), unique=True)
    website = db.Column(db.Unicode(255), unique=True)

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        return '<%s.%s %s>' % (self.__class__.__module__,
                               self.__class__.__name__, unicode(self))


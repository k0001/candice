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


import logging
import sys
import csv
from   candice.models import db, Candidate, Party, Charge


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

_cache = {}


def get_or_create_party(name):
    cache_key = 'party', name
    if not cache_key in _cache:
        created = True
        party = Party()
        party.name = name
        party.slug = name
        db.session.add(party)
        _cache[cache_key] = party
        log.info(u'Created Party %s' % repr(cache_key))
    else:
        created = False
        party = _cache[cache_key]
    return party, created


def get_or_create_charge(name, province=None, department=None, locality=None):
    cache_key = 'charge', name, province, department, locality
    if not cache_key in _cache:
        created = True
        charge = Charge()
        charge.name = name
        charge.province = province
        charge.department = department
        charge.locality = locality
        db.session.add(charge)
        _cache[cache_key] = charge
        log.info(u'Created Charge %s' % repr(cache_key))
    else:
        created = False
        charge = _cache[cache_key]
    return charge, created


def opt_text(text, encoding='utf-8'):
    """Returns decoded and striped text, or None if text is empty"""
    if text is None:
        return None
    if not isinstance(text, unicode):
        text = text.decode(encoding)
    return text.strip() or None


def import_csv(f):
    csv_reader = csv.DictReader(f)
    try:
        for row in csv_reader:
            c = Candidate()
            c.name = opt_text(row['Nombre'])
            c.slug = c.name
            c.party, _ = get_or_create_party(name=opt_text(row['Partido']))
            c.charge, _ = get_or_create_charge(
                name=opt_text(row['Cargo']),
                province=opt_text(row['Provincia']),
                department=opt_text(row['Departamento']),
                locality=opt_text(row['Localidad']))

            db.session.add(c)
            log.info(u'Created Candidate %s' % c.name)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        import_csv(f)




#!/usr/bin/env python
##############################################################################
#
#    Copyright (C) 2016 initOS GmbH (<http://www.initos.com>).
#    Author Nikolina Todorova <nikolina.todorova at initos.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import oerplib
import sys
import argparse
from datetime import datetime


def parse_args():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-s', '--server', metavar='HOST', dest='server',
                        default='localhost',
                        help="Odoo hostname.")

    parser.add_argument('-P', '--port', dest='port',
                        default='8069',
                        help="Odoo server port.")

    parser.add_argument('-r', '--rpc_protocoll', dest='protocol',
                        default='xmlrpc',
                        help="Odoo RPC protocoll.")

    parser.add_argument('-u', '--user', dest='user',
                        default='admin',
                        help="Odoo user name.")

    parser.add_argument('-p', '--pass', dest='passwd',
                        default='admin',
                        help="Odoo user password.")

    parser.add_argument('-d', '--database', dest='database',
                        default='db_name',
                        help="Odoo database name.")

    return parser.parse_args()

args = parse_args()
opts = dict(vars(args))

server_name = opts.get('server')
port = opts.get('port')
protocol = opts.get('protocol')

db = opts.get('database')
username = opts.get('user')
password = opts.get('passwd')

# Prepare the connection to the server
oerp = oerplib.OERP(server=server_name, protocol=protocol, port=port)

if db not in oerp.db.list():
    raise Exception('Unexisting db!')


# Login (the object returned is a browsable record)
user = oerp.login(username, password, db)


# get the names of all installed modules
def get_installed_modules():
    model = 'ir.module.module'
    domain = [('state', '=', 'installed')]
    fields = ['name']

    installed_modules_ids = oerp.search(model, domain)
    installed_modules = oerp.read(model, installed_modules_ids, fields)
    installed_modules_names = []
    for module in installed_modules:
        installed_modules_names.append(module['name'])
    return installed_modules_names

filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
try:
        file = open(filename1+'_installed_modules.txt', 'w')
        file.write('Version: ' + oerp.version + '\n')
        file.write('\n'.join(get_installed_modules()))
        file.close()

except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0)

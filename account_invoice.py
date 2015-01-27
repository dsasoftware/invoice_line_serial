# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class account_invoice_line(osv.osv):
        _name = 'account.invoice.line'
        _inherit = 'account.invoice.line'


        def retrieve_serial_number(self, cr, uid, ids, field_name, arg, context=None):
                records = self.browse(cr, uid, ids)
                picking_obj = self.pool.get('stock.picking')
                invoice_obj = self.pool.get('account.invoice')
                operation_obj = self.pool.get('stock.pack.operation')
                res = {}
                for r in records:
			invoice = invoice_obj.browse(cr,uid,r.invoice_id.id)
                        serial_number = 'N/A'
                        picking_ids = picking_obj.search(cr,uid,[('name','=',invoice.origin)])
			if picking_ids:
	                        for picking in picking_obj.browse(cr,uid,picking_ids):
        	                        if picking.pack_operation_ids:
						for pack_operation in picking.pack_operation_ids:
							if pack_operation.lot_id.name and pack_operation.product_id.id == r.product_id.id:
								serial_number = pack_operation.lot_id.name
				res[r.id] = serial_number		
			else:
	                        res[r.id] = 'N/A'
                return res

        _columns = {
                'serial_number': fields.function(retrieve_serial_number, type = 'char', string = 'Nro. Serie'),
                }

account_invoice_line()


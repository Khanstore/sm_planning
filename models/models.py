# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import date, datetime, time
import calendar
from dateutil import relativedelta
from odoo.osv.expression import get_unaccent_wrapper
import re

class resPartner(models.Model):
    _inherit = 'res.partner'
    is_site=fields.Boolean("Is a site")
class PlanningRole(models.Model):
    _inherit = 'planning.role'

    description =fields.Char("Description")
class planningSlot(models.Model):
    _inherit = "planning.slot"
    site_id=fields.Many2one('res.partner',string="Site")

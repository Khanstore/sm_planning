# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from collections import defaultdict
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


    def _group_slots_by_role(self):
        grouped_slots = defaultdict(self.browse)
        for slot in self.sorted(key=lambda s: s.role_id.name or ''):
            grouped_slots[slot.role_id] |= slot
        return grouped_slots
    def totalAllocatedHours(self):
        total=0
        for rec in self:
            total=total+rec.allocated_hours
        return total



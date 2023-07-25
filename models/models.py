# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import date, datetime, time
from odoo.osv.expression import get_unaccent_wrapper
import re


class planningSlot(models.Model):
    _inherit = "planning.slot"
    agent_id=fields.Many2one('res.partner',string="agent")

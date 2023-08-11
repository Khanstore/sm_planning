# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import date, datetime, time
import calendar
from dateutil import relativedelta
from odoo.osv.expression import get_unaccent_wrapper
import re

class PlanningRole(models.Model):
    _inherit = 'planning.role'

    description =fields.Char("Description")
class planningSlot(models.Model):
    _inherit = "planning.slot"
    agent_id=fields.Many2one('res.partner',string="agent")
class SMplanningSlot(models.TransientModel):
    _name = "sm.swis.report"

    resource_ids=fields.Many2many('resource.resource',string="Resource")

    def get_years():
        year_list = []
        # y=date.today().year
        y= date.today().year
        for i in range(y-2, y+2):
            year_list.append((str(i), str(i)))
        return year_list

    # Inside the model
    month = fields.Selection([('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                              ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
                              ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December'), ],
                             string='Month')
    year=fields.Selection(get_years(),default='datetime.today.year', string='Year', )

    day_in_month=fields.Integer("days In Month", compute="get_days_in_month")


    def get_days_in_month(self):
        for rec in self:
            if rec.month and rec.year:
                rec.day_in_month=calendar.monthrange(int(rec.year), int(rec.month))[1]

    def resources(self):
        for rec in self:
            if len(rec.resource_ids)>0:
                res=self.env['planning.slot'].search([('resource_id','in',rec.resource_ids.ids)])
                return res
            else:
                res=self.env['planning.slot'].search([])
                return res

    def _get_report_values(self, docids, data=None):
        if len(rec.resource_ids) > 0:
            res = self.env['planning.slot'].search([('resource_id', 'in', rec.resource_ids.ids)])

        else:
            res = self.env['planning.slot'].search([])

        return {
            'doc_ids': self.ids,
            'planning_slots':res,
        }

class SmSwissReport(models.AbstractModel):
    _name = 'report.sm_planning.sm_swis_report'

    def get_report_paperformat(self, docids, data=None):
        return self.env.ref('report.paperformat_custom_format').sudo()
    def get_data(self,res): #here res is planning.slot in the date range
        data={}
        data['persons']= {}
        data['totals']= {}
        for rec in res:
            person_id=rec.resource_id
            agent_id = rec.agent_id
            date_day = rec.start_datetime.day
            agent_data = {}
            date_data = {}
            if date_day in data['totals']:
                data['totals'][date_day]=data['totals'][date_day]+rec.allocated_hours
            else:data['totals'][date_day]=rec.allocated_hours


            if not person_id in data['persons']:
                personal_data = {}
                # todo customise string for printing
                string=rec.role_id.name +'\n'+str(rec.start_datetime.hour)+":"+ str(rec.start_datetime.strftime('%M'))+"\n" + str(rec.end_datetime.hour)+":"+ str(rec.end_datetime.strftime('%M'))
                date_data[date_day]=string
                agent_data[agent_id]=date_data
                data['persons'][person_id]=agent_data
            elif not agent_id in data['persons'][person_id]:  # new agent for person
                # todo customise string for printing
                string=rec.role_id.name +'\n'+str(rec.start_datetime.hour)+":"+ str(rec.start_datetime.minute)+"\n" + str(rec.end_datetime.hour)+":"+ str(rec.end_datetime.minute)
                date_data[date_day]=string
                # agent_data[agent_id]=date_data
                data['persons'][person_id][agent_id]=date_data
            elif not date_day in data['persons'][person_id][agent_id]:
                string =rec.role_id.name +'\n'+ str(rec.start_datetime.hour)+":"+ str(rec.start_datetime.minute)+"\n" + str(rec.start_datetime.hour)+":"+ str(rec.start_datetime.minute)
                # date_data[date_day] = string
                data['persons'][person_id][agent_id][date_day]=string

        return data
    def get_roles(self,res):
        roles = []
        for rec in res:
            if not rec.role_id in roles:
                roles.append(rec.role_id)
        return roles




    def _get_report_values(self, docids, data=None):
        doc=self.env['sm.swis.report'].search([('id','=',docids[0])])
        wizard=self.env['sm.swis.report'].search([('id','in',docids)])
        month=wizard.month
        year=wizard.year
        days_in_month=calendar.monthrange(int(wizard.year), int(wizard.month))[1]
        start_date=datetime(int(wizard.year), int(wizard.month),1)
        end_date=(start_date + relativedelta.relativedelta(months=1)).replace(day=1)

        if len(wizard.resource_ids.ids) > 0:
            res = self.env['planning.slot'].search([('resource_id', 'in', wizard.resource_ids.ids),('start_datetime', '>',start_date),('start_datetime', '<',end_date)])
        else:
            res = self.env['planning.slot'].search([('start_datetime', '>',start_date),('start_datetime', '<',end_date)])



        return {
            'docids': doc,
            'planning_slots':res,
            'month':month,
            'year':year,
            'days_in_month':days_in_month,
            'data':self.get_data(res),
            'roles':self.get_roles(res),
        }
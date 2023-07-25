# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class PMIS(http.Controller):


    @http.route('/my/pims', type='http',auth="user",website=True)
    def pims_report(self):
        partner=request.env.user.partner_id
        return request.render('pmis.pmis_portal_report',{'docs':partner})
    @http.route('/my/pims/edit', type='http',auth="user",website=True)
    def pims_edit(self):
        partner=request.env.user.partner_id
        return request.render('pmis.portal_pmis_edit',{'docs':partner})
    @http.route('/contacts', type='http',auth="user",website=True)
    def contact(self):
        partner=request.env.user.partner_id
        return request.render('pmis.pmis_portal_report',{'docs':partner})
        # return partner.name
    @http.route('/thankyou', type='http', auth="public", website=True)
    def thankyou(self):
        return request.render('pmis.thank_you', {})

    @http.route('/search_contacts', type='http', auth="public", website=True)
    def search_contacts(self):
        return request.render('pmis.search_contacts', {})

    @http.route('/searching_contacts', type='http', auth="public", website=True)
    def searching_contacts(self,**post):
        search_str=post.get('name')
        contacts=request.env['res.partner'].search([("name".lower(),"like",search_str)])
        print(search_str)
        return request.render('pmis.contacts',{'conta':contacts})
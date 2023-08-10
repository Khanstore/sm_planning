# -*- coding: utf-8 -*-



{
    'name': "Palaning By SM",

    'summary': """
        Project for Swis Client""",

    'description': """
        design a reporting app for Swiss Client
    """,

    'author': "SM Ashraf",
    'website': "https://www.khan-store.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','planning'],

    # always loaded
    'data': [
        "reports/reports.xml",

        "views/views.xml",
        "security/ir.model.access.csv",

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],


    "auto_install": False,
    'application': True,
    'license': 'LGPL-3',
    "installable": True,
}

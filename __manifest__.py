# -*- coding: utf-8 -*-
{
    'name': "odoo_basico",

    'summary': """
        Exemplos dos tipos de datos a utilizar """,

    'description': """
       Exemplos dos tipos de datos a utilizar e vistas,menús....
    """,

    'author': "Antonio",
    'website': "https://www.edu.xunta.gal/centros/iesteis/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/informacion.xml',
        'views/cabeceira.xml',
        'views/linea.xml',
        'views/templates.xml',
        'views/report_header.xml',
        'views/report_informacion.xml',
        'views/menu.xml',
        'security/xestion_usuarios.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license' : 'AGPL-3',
    'installable': True,
    'application': True,
}
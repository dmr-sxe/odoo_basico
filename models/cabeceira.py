# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cabeceira (models.Model):
    _name="odoo_basico.cabeceira" # Será o nome da táboa
    _description = "Modelo cabeceira"
    _sql_constraints = [('nome_unico', 'unique(name)', 'Non se pode repetir o Identificador')]

    name = fields.Char(required=True, size=20, string="Identificador")
    linea_ids = fields.One2many("odoo_basico.linea",'cabeceira_id') # Os campos One2many Non se almacena na BD
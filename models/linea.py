# -*- coding: utf-8 -*-

from odoo import models, fields, api

class linea (models.Model):
    _name="odoo_basico.linea" # Será o nome da táboa
    _description = "Modelo linea"

    descripcion_da_linea = fields.Text(string="A Descripción")
    cabeceira_id = fields.Many2one('odoo_basico.cabeceira',ondelete= "cascade",required=True)
    # informacion_ids = fields.Many2many("odoo_basico.informacion") 
    # Os campos Many2many crean unha táboa na BD
    informacion_ids = fields.Many2many("odoo_basico.informacion",string="Rexistro de Información",
                                       relation="odoo_basico_linea_informacion",
                                       column1="linea_id",column2="informacion_id",ondelete="set null")

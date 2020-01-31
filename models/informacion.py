# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class informacion (models.Model):
    _name="odoo_basico.informacion" # Será o nome da táboa
    _description = "Tipos de datos básicos"
    _sql_constraints = [('nome unico', 'unique(name)', 'Non se pode repetir o nome')]

    name = fields.Char(required=True,size=20,string="Titulo")
    descripcion = fields.Text(string="A Descripción")# string é a etiqueta do campo
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string='Sexo')
    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_mes = fields.Text(compute="_mes_data", size=15, store=True)
    data_hora = fields.Datetime(string="Hora", default=lambda self: fields.Datetime.now())
    alto_en_cms = fields.Integer(string="Alto en centímetros")
    longo_en_cms = fields.Integer(string="Longo en centímetros")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros")
    volume = fields.Float(compute="_volume", store=True)
    volume_entre_100 = fields.Float(compute="_volume_entre_100", store=False)
    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)
    densidade = fields.Float(compute="_densidade", store=True)
    # Os campos Many2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency',domain="[('position','=','after')]") 
    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    gasto = fields.Monetary("Gasto", 'moeda_id')
    foto = fields.Binary(string="Foto")
    nome_adxunto = fields.Char(size=20, string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo Adxunto")

    moeda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto",store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)



    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms)

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume_entre_100(self):
        for rexistro in self:
            rexistro.volume_entre_100 = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms))/100

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume !=0:
                rexistro.densidade = 100 * (float(rexistro.peso) / float(rexistro.volume))
            else:
                rexistro.densidade = 0

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):   # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

    @api.depends('data')
    def _mes_data(self):
        for rexistro in self:
            rexistro.data_mes = rexistro.data.strftime("%B")



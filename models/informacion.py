# -*- coding: utf-8 -*-
import locale

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import pytz

class informacion (models.Model):
    _name="odoo_basico.informacion" # Será o nome da táboa
    _description = "Tipos de datos básicos"
    _order = "data_hora desc"
    _sql_constraints = [('nome unico', 'unique(name)', 'Non se pode repetir o nome')]

    name = fields.Char(required=True,size=20,string="Titulo")
    descripcion = fields.Text(string="A Descripción")# string é a etiqueta do campo
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string='Sexo')
    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    mes_data = fields.Char(compute="_mes_data", size=15, store=True)
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    hora_utc  = fields.Char(compute="_hora_utc",string="Hora UTC", size=15, store=True)
    hora_usuario  = fields.Char(compute="_hora_usuario",string="Hora Usuario", size=15, store=True)
    mes_castelan = fields.Char(compute="_mes_castelan", size=15, store=True)
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
        locale.setlocale(locale.LC_TIME, "gl_ES.utf8")
        for rexistro in self: #O idioma é o configurado en locale na máquina de odoo
            rexistro.mes_data = rexistro.data.strftime("%B")

    @api.depends('data')
    def _mes_castelan(self):
        locale.setlocale(locale.LC_TIME, "es_ES.utf8")
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B")

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self: # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    @api.depends('data_hora')
    def _hora_usuario(self):
        for rexistro in self:  # Convertimos a hora UTC a hora do usuario
            self.actualiza_hora()

    def ver_contexto(self): # Engadimos na vista un button no header. O name do button é o nome da función
        for rexistro in self: #Ao usar warning temos que importar a libreria from odoo.exceptions import Warning
            raise Warning('Contexto: %s' % rexistro.env.context) #env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(self.env.user.tz or 'UTC')  # obter a zona horaria do usuario
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)  # hora co horario do usuario en formato object

    def data_hora_local(self):
        data_hora_usuario_object = self.convirte_data_hora_de_utc_a_timezone_do_usuario(fields.Datetime.now())
        for rexistro in self:
            data_hora_do_campo_da_bd = self.convirte_data_hora_de_utc_a_timezone_do_usuario(rexistro.data_hora)
            raise Warning('Datetime.now() devolve a hora UTC %s cambiamola coa configuración horaria do usuario %s cambiamos tamén a do campo data_hora %s'
                       % (fields.Datetime.now().strftime ('%Y-%m-%d %H:%M'),data_hora_usuario_object,data_hora_do_campo_da_bd))
        return True

    def actualiza_hora(self):
        for rexistro in self:
            rexistro.hora_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(rexistro.data_hora).strftime(
                "%H:%M:%S")
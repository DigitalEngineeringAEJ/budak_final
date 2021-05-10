# -*- coding: utf-8 -*-

from odoo import api, fields, models, _ 
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
from odoo import exceptions
from odoo.exceptions import UserError

class my_module(models.Model):
    _name = 'my_module.my_module'
    _description = 'my_module.my_module'
        
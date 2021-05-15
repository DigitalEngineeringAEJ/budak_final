# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta

class aej_gutachten(models.Model):
     _name = 'aej_gutachten.aej_gutachten'
     _description = 'aej_gutachten.aej_gutachten'
     _inherit = 'project.task'
    stage_id = fields.Many2one('project.task.type', 'stageXXX')
    currentDay = datetime.now().day
    currentMonth = datetime.now().month 
    currentYear = datetime.now().year

    #Suchfunktion für Ordnerstruktur 
#    wortliste = [str(currentYear),str(currentMonth)]
#    trennzeichen = ' / '
#    suchordner = str(trennzeichen.join(wortliste))
    
    #testfeld = fields.Char(string="Testfeld", default="Test", store=False)
    
    
    #Unterordner anlegen, wenn neuer Kunden zu einer Aufgabe hinzugefügt wird
#    @api.onchange('partner_id')
#    def _create_customerfolder(self):
#        if self.partner_id:
#            if not self.env['documents.folder'].search([('display_nameXX', 'like', self.partner_id.name)]):
#                self.env['documents.folder'].create({
#                    'name':self.partner_id.name + self.suchordner,
#                    'parent_folder_id': self.env['documents.folder'].search([('display_nameXX', '=', self.suchordner)]).id
                
#            })
    
    
#    @api.onchange('stage_id')
#    def _onchangestage(self):
#        if self.stage_id.display_name == 'Fertig':
#            self.env['documents.document'].create({
#                'name': self.message_main_attachment_id.name,
#                'type': 'binary',
#                'datas': self.message_main_attachment_id.datas,
#                'folder_id': self.env['documents.folder'].search([('display_nameXX', 'like', self.partner_id.name + self.suchordner)]).id,
#                'partner_id':self.partner_id.id
#        })
    
    #Validierungsfehler wenn kein Anhang da ist
#    @api.onchange('stage_id')
#    def _check_attachment(self):
#        if not self.message_main_attachment_id:
#            message = _('Anhang von %s und Kunde %s fehlt') % (self.name, self.partner_id.name)
#            raise UserError(message) 
            
    #Validierungsfehler wenn kein Kunde da ist
#    @api.onchange('stage_id')
#    def _check_customer(self):
#        if not self.partner_id:
#            return {
#                'warning': {
#                'title': 'Warning!',
#                'message': 'Kein Kunde!!!!!!!!!!'}    
#            }


            
    
        
#Der normale Display name funktioniert nicht --> Muss store = True sein        
#class aej_folder2(models.Model):
#    _inherit = 'documents.folder'
#    display_nameXX = fields.Char(related='display_name' ,string='DisplayNameX', store=True)

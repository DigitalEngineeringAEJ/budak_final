# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import exceptions
from odoo.exceptions import UserError

class aej_document(models.Model):
    _inherit = 'project.task'
    stage_id = fields.Many2one('project.task.type', 'stageXXX')
    
    
    #folder_id --> Siehe Jahr (entfällt ggf. )
        # Monat (entfällt ggf. )
            #Haftpflichtschadengutachten
                #Kunde
    
    
    @api.onchange('stage_id')
    def _onchangestage(self):
        self.kanban_state = 'done'
        #self.message_main_attachment_id.unlink() 
        #raise UserError("message")
        if self.stage_id.display_name == 'Fertig':
            self.env['documents.document'].create({
                'name': self.message_main_attachment_id.name,
                'type': 'binary',
                'datas': self.message_main_attachment_id.datas,
                'folder_id':1,
                'partner_id':self.partner_id.id
        })
        
    @api.onchange('stage_id')
    def _check_attachment(self):
        if not self.message_main_attachment_id:
            #raise exceptions.ValidationError(_("Kein Anhang!"))
            message = _('Anhang von %s und Kunde %s fehlt') % (self.name, self.partner_id.name)
            raise UserError(message) 
      #  if self.stage_id.display_name == 'Fertig':
      #      message = _('Moving from %s to %s is not allowd') % (self.stage_id.id, self.stage_id.display_name)
      #      raise UserError(message) 
    
    @api.onchange('stage_id')
    def _check_customer(self):
        if not self.partner_id:
            return {
                'warning': {
                'title': 'Warning!',
                'message': 'Kein Kunde!!!!!!!!!!'}    
            }
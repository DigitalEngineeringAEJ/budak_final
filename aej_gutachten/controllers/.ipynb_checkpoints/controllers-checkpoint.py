# -*- coding: utf-8 -*-
# from odoo import http


# class AejGutachten(http.Controller):
#     @http.route('/aej_gutachten/aej_gutachten/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aej_gutachten/aej_gutachten/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aej_gutachten.listing', {
#             'root': '/aej_gutachten/aej_gutachten',
#             'objects': http.request.env['aej_gutachten.aej_gutachten'].search([]),
#         })

#     @http.route('/aej_gutachten/aej_gutachten/objects/<model("aej_gutachten.aej_gutachten"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aej_gutachten.object', {
#             'object': obj
#         })

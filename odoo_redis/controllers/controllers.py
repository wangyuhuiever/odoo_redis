# -*- coding: utf-8 -*-
# from odoo import http


# class OdooRedis(http.Controller):
#     @http.route('/odoo_redis/odoo_redis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_redis/odoo_redis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_redis.listing', {
#             'root': '/odoo_redis/odoo_redis',
#             'objects': http.request.env['odoo_redis.odoo_redis'].search([]),
#         })

#     @http.route('/odoo_redis/odoo_redis/objects/<model("odoo_redis.odoo_redis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_redis.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-

from odoo import models, fields


class IrModelField(models.Model):
    _inherit = 'ir.model.fields'

    redis_key = fields.Integer(
        string="Save Redis Key",
        help="If redis key more than 1, will auto join with semicolon order by value",
    )
    redis_value = fields.Boolean(
        string="Enable Save Redis",
        help="If set this parameter to true, value will be stored in redis.",
    )


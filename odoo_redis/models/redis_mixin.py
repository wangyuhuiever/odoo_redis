# -*- coding: utf-8 -*-

from odoo import models, tools, api
from odoo.tools import config
import redis
import json
import logging

_logger = logging.getLogger(__name__)


class RedisMixin(models.AbstractModel):
    _name = 'redis.mixin'

    @tools.ormcache('self', 'name')
    def _get_redis_fields(self, name):
        """ Return the set of tracked fields names for the current model. """
        fields = {
            field
            for field in self._fields.values()
            if getattr(field, name, None)
        }

        return fields

    @api.model
    def get_redis_client(self, db_name):
        redis_host = config.get('redis_host')
        redis_port = config.get('redis_port')
        redis_password = config.get('redis_password')
        redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=db_name)
        return redis_client

    def set_pipeline_redis_cache(self, data):
        redis_cache_prefix = config.get('redis_cache_prefix', '')
        client = self.get_redis_client(config.get('redis_cache_db', '0'))
        redis_pipeline = client.pipeline(transaction=False)

        step = 1000
        for i in range(0, len(data), step):
            values = data[i:i+step]
            for d in values:
                for k, v in d.items():
                    redis_pipeline.set('{}:{}'.format(redis_cache_prefix, k), json.dumps(v))
            try:
                _logger.info(values)
                redis_pipeline.execute()
            except Exception as e:
                _logger.error('sync redis failed: {}'.format(e))

    def write(self, vals):
        res = super(RedisMixin, self).write(vals)
        if res:
            values = []
            for rec in self:
                rk = self._get_redis_fields('redis_key')
                rk = sorted(rk, key=lambda x: x.redis_key)
                key_values = []
                for field in rk:
                    key_values.append(getattr(rec, field.name, None))
                redis_key = ':'.join(key_values)
                rv = self._get_redis_fields('redis_value')
                data = {}
                for field in rv:
                    data.update({
                        field.name: getattr(rec, field.name, None)
                    })
                values.append({redis_key: data})
            _logger.info(values)
            self.set_pipeline_redis_cache(values)
        return res

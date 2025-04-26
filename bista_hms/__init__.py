# -*- coding: utf-8 -*-

from . import models
from . import wizard

def update_record_rule(env):
    print("Updating record rule====================")
    sale_rule_id = env.ref('sale.sale_order_personal_rule')
    sale_rule_id.write({
        'perm_create' : True,
        'perm_write' : True,
        'perm_unlink' : False,
        'perm_read' : True
    })

from django import template

import json
import ast

register = template.Library()

@register.filter
def load_json(data):
    eval_json = ast.literal_eval(data)
    return eval_json.items()

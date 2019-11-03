import json

from django import template

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


register = template.Library()


@register.filter
def pretty_json(value):
    return highlight(json.dumps(value, indent=4), JsonLexer(), HtmlFormatter())

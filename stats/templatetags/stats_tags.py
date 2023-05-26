import json

from django import template

register = template.Library()


@register.filter(name='js_data')
def js_data(value):
    return json.dumps(value)


@register.simple_tag(name='get_stat_item')
def get_stat_item(subject, student):
    return stat_item.first() if hasattr(subject, 'statistic') and (stat_item := subject.statistic.statisticitem_set.filter(student=student)).exists() else None


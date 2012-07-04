import datetime
import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import widgets
from django.forms.widgets import Widget, Select
from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


__all__ = ('TinyWidget', 'TinyAdminWidget', 'RadioSelect', )


class TinyWidget(forms.Textarea):
    config = {
    }

    def __init__(self, attrs=None, config=None):
        self.config.update(config or {})
        super(TinyWidget, self).__init__(attrs)

    def render(self, name, value, attrs):
        editor_selector = 'tiny-%s' % attrs['id']
        attrs['class'] = editor_selector
        self.config['editor_selector'] = editor_selector
        s = super(TinyWidget, self).render(name, value, attrs)
        return s + render_to_string('util/tiny.html', {
            'MEDIA_URL': settings.MEDIA_URL,
            'config': simplejson.dumps(self.config),
        })

    class Media:
        js = (
            'tiny_mce/tiny_mce.js',
            'js/tiny_config.js',
        )

class TinyAdminWidget(TinyWidget):
    config = {
        # cant seem to be able to user reverse here
        # 'external_image_list_url': reverse('admin:images_image_imagelist'),
        'external_image_list_url': '/admin/images/image/imagelist/',
    }


class RadioFieldRenderer(widgets.RadioFieldRenderer):
    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        html = []
        for w in self:
            html.append('<li>%s</li>' % force_unicode(w))
        return mark_safe(u'<ul class="radiolist">\n%s\n</ul>' % u'\n'.join(html))


class RadioSelect(widgets.RadioSelect):
    renderer = RadioFieldRenderer




__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.

    Based on SelectDateWidget, in 

    django/trunk/django/forms/extras/widgets.py


    """
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = MONTHS.items()
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)


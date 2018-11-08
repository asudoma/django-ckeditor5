from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.forms.widgets import get_default_renderer
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from js_asset import JS, static


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


json_encode = LazyEncoder().encode

DEFAULT_CONFIG = {
    'height': 200,
    'width': 1000
}


class CKEditorWidget(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """

    class Media:
        js = (
            JS('ckeditor5/ckeditor-init.js', {
                'id': 'ckeditor-init-script',
                'data-ckeditor-basepath': getattr(
                    settings,
                    'CKEDITOR_BASEPATH',
                    static('ckeditor5/ckeditor/'),
                ),
            }),
            'ckeditor5/ckeditor/ckeditor.js',
            'ckeditor5/ckeditor/translations/ru.js'
        )

    def __init__(self, config_name='default', *args, **kwargs):
        super(CKEditorWidget, self).__init__(*args, **kwargs)
        # Setup config from defaults.
        self.config = DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, 'CKEDITOR5_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if config_name in configs:
                    config = configs[config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('CKEDITOR5_CONFIGS["%s"] \
                                setting must be a dictionary type.' %
                                                   config_name)
                    # Override defaults with settings config.
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                            found in your CKEDITOR5_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('CKEDITOR5_CONFIGS setting must be a\
                        dictionary type.')

    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ''
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)

        return mark_safe(renderer.render('ckeditor/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_text(value)),
            'id': final_attrs['id'],
            'config': json_encode(self.config),
        }))

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

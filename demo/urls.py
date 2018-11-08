from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from .demo.views import ckeditor_form_view

urlpatterns = [
                  url(r'^$', ckeditor_form_view, name='ckeditor-form'),
                  url(r'^admin/', admin.site.urls),
              ] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

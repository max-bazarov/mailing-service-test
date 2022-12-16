from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += doc_urls
urlpatterns += [
    path('', RedirectView.as_view(pattern_name='schema-swagger-ui'))
]

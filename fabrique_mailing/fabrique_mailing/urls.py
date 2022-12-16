from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('mailings.urls')),
]


urlpatterns += doc_urls
urlpatterns += [
    path('', RedirectView.as_view(pattern_name='schema-swagger-ui'))
]

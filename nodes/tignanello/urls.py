from django.conf.urls import url, include

urlpatterns = [
    url(r'^tap/', include('vamdctap.urls')),
]

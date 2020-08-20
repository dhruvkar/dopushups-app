from django.conf.urls import url

from . import views


urlpatterns = [
    url('', views.sms_response, name='sms'),

]
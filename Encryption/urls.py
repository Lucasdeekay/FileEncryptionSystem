from django.urls import path

from Encryption import views
from Encryption.views import EncryptView

app_name = "Encryption"

urlpatterns = [
    path("", EncryptView.as_view(), name="home"),
    path('decrypt', views.decrypt_file, name='decrypt'),
]

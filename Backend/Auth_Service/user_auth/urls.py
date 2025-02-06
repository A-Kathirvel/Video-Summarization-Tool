from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',signup),
    path('signin/',signin),
    path("getuserdetails/",getUserdetails),
    path("updatepassword/",updatePassword),
    path("getvideodetials/",getVideoDetials)
]

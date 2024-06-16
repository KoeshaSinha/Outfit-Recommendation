"""
URL configuration for outfit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#add these for media url
from django.conf import settings
from django.conf.urls.static import static

from recommendation.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='homepage'),
    path('aboutus', aboutus),
    path('explore', explore),
    path('tips', tips),
    path('login/', login, name = 'login'),
    path('signup/', signup, name='signup'),
    path('contact', contact),
    path('upload/', upload_images, name='upload_images'),
    path('upload2/', upload_images2, name='upload_images2'),
    path('user_home/(?P<username>\w+)/$', user_home, name='user_home'),
    path('upload_view/', upload_view, name='upload_view'),
    path('upload_view2/', upload_view2, name='upload_view2'),
    path('previous_outfits/', previous_outfits, name='previous_outfits'),
    path('previous_outfits2/', previous_outfits2, name='previous_outfits2'),
    path('predictions/', predictions, name='predictions'),
    path('predictions2/', predictions2, name='predictions2')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#(?P<username>\w+)/$

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



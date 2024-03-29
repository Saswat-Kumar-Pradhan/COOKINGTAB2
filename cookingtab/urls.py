"""
URL configuration for cookingtab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginSignup, name='loginSignup'),
    path('home', home, name='home'),
    path('addProfile', addProfile, name='addProfile'),
    path('profileDetails/<int:profile_id>', profileDetails, name='profileDetails'),
    path('editProfileDetails/<int:profile_id>', editProfileDetails, name='editProfileDetails'),
    path('deleteProfileDetails/<int:profile_id>', deleteProfileDetails, name='deleteProfileDetails'),
    path('eventDetails/<int:event_id>/<int:y>', eventDetails, name='eventDetails'),
    path('editEventDetails/<int:event_id>/<int:y>', editEventDetails, name='editEventDetails'),
    path('deleteEventDetails/<int:event_id>', deleteEventDetails, name='deleteEventDetails'),

    path('timer', timer, name='timer'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
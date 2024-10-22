"""
URL configuration for Voting_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from voting.views import home1 

from django.contrib import admin
from django.urls import path, include
from voting.views import home1  # Use the correct view name
app_name = 'accounts'
urlpatterns = [
    path('', home1, name='home'),
    path("accounts/", include("accounts.urls")),   # Set the root URL to the home page view
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("voting/", include("voting.urls", namespace="voting")),  # Add namespace here
    
]

    #path('',include('voting.urls')),path("", home1, name="home"),path("", home1, name="home"),
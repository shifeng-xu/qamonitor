"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from common import views as common_views
from quality import views as quality_views
from common import jiraspider

urlpatterns = [
    path('index/', common_views.index),
    path('admin/', admin.site.urls),
    path('login/',common_views.login),
    path('logout/',common_views.logout),
    path('monitorTable/',common_views.monitorTable),
    path('table/',common_views.table),
    path('readlog/',common_views.readlog),
    path('updatedatabase/',jiraspider.getjRoles),
    path('updateComponents/',jiraspider.getComponents),

    path('quality/bugsoffline',quality_views.bugsoffline),
    path('quality/bugsoffline/getItems',quality_views.getItems),
    path('quality/bugsoffline/getRepairedRrate',quality_views.getRepairedRrate),
    path('quality/bugsoffline/getRepairedRrateByGroup',quality_views.getRepairedRrateByGroupOffline),

    path('quality/bugsonline',quality_views.bugsonline),
    path('quality/bugsonline/getRepairedRrateByGroup',quality_views.getRepairedRrateByGroupOnline),


]

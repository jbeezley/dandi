"""dandi URL Configuration

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
import debug_toolbar

from django.contrib import admin
from django.urls import include, path

from djaunty.api import DataTagViewSet, DatasetViewSet
from djaunty.views import dataset, search, text_search, tree

from rest_framework import routers


router = routers.DefaultRouter()
router.register('datasets', DatasetViewSet)
router.register('datatags', DataTagViewSet)

urlpatterns = [
    path('__debug__', include(debug_toolbar.urls)),
    path('text/', text_search),
    path('search/', search),
    path('tree/', tree),
    path('datasets/<int:id>/', dataset),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

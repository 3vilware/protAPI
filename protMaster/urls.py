"""protMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from protAPI import views
from rest_framework import routers
from django.conf.urls.static import static
from protMaster import settings
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
# router.register(r'rest/<int:id>', views.UserViewSet.as_view())

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', views.index),
    path('testing', views.TestEndpoint.as_view()),
    # path('rest', views.UserViewSet.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('api/', include(router.urls)),
    path('rest/<int:pk>', views.UserViewSet.as_view(), name="viewUser"),
    path('rest', views.UserViewSetAll.as_view(), name="viewUserAll"),
    # path('job/<int:pk>', views.JobViewSetAll.as_view(), name="Jobv"),
    path('job', views.JobViewSetAll.as_view(), name="jobviewUserAll"),
    path('run_job', views.RunJob.as_view(), name="run_job"),

    path('view_prot/<str:name>', views.viewProt, name="viewProt"),

    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.Register.as_view(), name='register'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
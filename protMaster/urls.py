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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
# router.register(r'rest/<int:id>', views.UserViewSet.as_view())

schema_view = get_schema_view(
   openapi.Info(
      title="Proteins API",
      default_version='v1',
      description="Documentation for protein api",
      terms_of_service="",
      contact=openapi.Contact(email="ricardoamadorcast@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test', views.index),
    path('testing', views.TestEndpoint.as_view()),
    # path('rest', views.UserViewSet.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('api/', include(router.urls)),
    # path('rest/<int:pk>', views.UserViewSet.as_view(), name="viewUser"),
    # path('rest', views.UserViewSetAll.as_view(), name="viewUserAll"),
    # path('job/<int:pk>', views.JobViewSetAll.as_view(), name="Jobv"),
    # path('job', views.JobViewSetAll.as_view(), name="jobviewUserAll"),
    path('run_job', views.RunJob.as_view(), name="run_job"),
    path('models', views.ModeltrainedViewSet.as_view(), name="models"),
    path('models/<int:pk>', views.ModelTrainedChange.as_view(), name="models"), # delete/update
    path('protein_data/<str:protein_id>', views.ProteinData.as_view(), name="protein_data"), # delete/update

    path('view_prot/<str:name>', views.viewProt, name="viewProt"),

    path('index', views.index, name='index'),
    path('sendCode', views.generateModel, name='sendCode'),
    path('login', obtain_auth_token, name='api_token_auth'),
    path('register/', views.Register.as_view(), name='register'),

    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api_samples/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
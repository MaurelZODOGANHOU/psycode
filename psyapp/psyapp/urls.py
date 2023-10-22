from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.views import (
    PsyListCreateView,
    PsyRetrieveUpdateDestroyView,
    LieuConsultationListCreateView,
    LieuConsultationRetrieveUpdateDestroyView,
    CabinetListCreateView,
    CabinetRetrieveUpdateDestroyView,
    PatientListCreateView,
    PatientRetrieveUpdateDestroyView
)

from accounts.views import UserCreateView, TypeConsultationListView

from zoomapp.views import CommunicationView

from zoomapp.views import VideoCallListCreateView, VideoCallDetailView, GenerateVideoToken

from zoomapp.views import AppelClientTwilioListCreateView, AppelClientTwilioDetailView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), )

router = DefaultRouter()

urlpatterns = [
    # authentication
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register/', UserCreateView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # appel audio and sms call
    # path('start-audio-call/', AudioCallView.as_view(), name='start-audio-call'),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls'))

    path('appels/', AppelClientTwilioListCreateView.as_view(), name='appel-list-create'),
    path('appels/<int:pk>/', AppelClientTwilioDetailView.as_view(), name='appel-detail'),

    path('start-sms-com/', CommunicationView.as_view(), name='start-communication'),

    # Appel video suivi de génératio  de token
    path('video-calls/', VideoCallListCreateView.as_view(), name='video-call-list-create'),
    path('video-calls/<int:pk>/', VideoCallDetailView.as_view(), name='video-call-detail'),
    path('generate-token/', GenerateVideoToken.as_view(), name='generate-token'),

    # filters
    path('type-consultation/', TypeConsultationListView.as_view(), name='type-consultation-list'),

    # servvices connexee

    path('psy/', PsyListCreateView.as_view(), name='psy-list-create'),
    path('psy/<int:pk>/', PsyRetrieveUpdateDestroyView.as_view(), name='psy-detail'),

    path('lieu/', LieuConsultationListCreateView.as_view(), name='lieu-list-create'),
    path('lieu/<int:pk>/', LieuConsultationRetrieveUpdateDestroyView.as_view(), name='lieu-detail'),

    path('cabinet/', CabinetListCreateView.as_view(), name='cabinet-list-create'),
    path('cabinet/<int:pk>/', CabinetRetrieveUpdateDestroyView.as_view(), name='cabinet-detail'),

    path('patient/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patient/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-detail'),

]

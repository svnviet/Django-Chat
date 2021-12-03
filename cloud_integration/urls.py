from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'cloud_integration'
urlpatterns = [
    path('', views.HomePage.as_view(), name='Home'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

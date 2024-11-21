from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import RegisterUserView, LoginUserView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/jwt/register/', RegisterUserView.as_view(), name="register"),
    path('api/auth/jwt/login/', LoginUserView.as_view(), name="login"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
from django.urls import path, include
from .views import RegistrationWithTokenView, LogoutView, Email
from rest_framework import routers
from .views import ComponentViewSet


router = routers.DefaultRouter()

router.register('component', ComponentViewSet, basename='component')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('token/login/', RegistrationWithTokenView.as_view(), name='token_create'),
    path('token/logout/', LogoutView.as_view(), name='logout'),
    path('activate/<str:uid>/<str:token>/', Email.as_view(), name='activate_account'),
]

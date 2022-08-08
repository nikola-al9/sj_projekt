from django.urls import path
from .views import AccountViewSet, UserLoginApiView, ChangePasswordView


urlpatterns = [
    path('accounts/', AccountViewSet.as_view()),
    path('accounts/<int:pk>/', AccountViewSet.as_view()),
    path('login/', UserLoginApiView.as_view(), name="login"),
    path('password-reset/', ChangePasswordView.as_view(), name='request-password-reset'),
]

from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import *

from .REST.views.users_views import *
from .views.all_views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    # API:
    path('register/', RegisterView.as_view(), name="register"),
    path('register_done/', RegisterDoneView.as_view(), name="register_email_link"),

    path('reset/', ResetView.as_view(), name="reset"),
    path('reset_ok/', ResetOKView.as_view(), name="reset_email_link"),
    path('reset_done/', ResetDoneView.as_view(), name="enter_new_password"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    path('user/', BasicUserView.as_view()),
    path('edit/', EditUserView.as_view()), #edits everything
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('promote/<uuid:id>/', PromoteView.as_view()),

    # ARCHIVED:
    # path('landing/', landing, name='fake_landing'),
    # path('register/', register, name='register'),
    # path('login/', LoginView.as_view(),
    #      name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # url(r'^activate/'
    #     r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
    #     r'(?P<token>[0-9A-Za-z]{1,13}'
    #     r'-[0-9A-Za-z]{1,20})/$', register_complete, name='register_complete'),
    # path('change/', PasswordChangeView.as_view(template_name='password_change.html',
    #                                            success_url=reverse_lazy('fake_landing')),
    #                                            name='change'),
    # path('reset/', PasswordResetView.as_view(template_name='reset.html',
    #                                          # html_email_template_name = "reset_email.html",
    #                                          success_url=reverse_lazy('reset_done')), name='reset'),
    # path('reset_done/', PasswordResetDoneView.as_view(template_name='reset_done.html'),
    #      name='reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset_confirm.html'),
    #      name='password_reset_confirm'),
    # path('reset_complete/', PasswordResetCompleteView.as_view(template_name='reset_complete.html'),
    #      name='reset_complete'),

]

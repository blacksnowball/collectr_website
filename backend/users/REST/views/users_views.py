from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions

import jwt
from ..serializers.users_serializers import *
from ...extras import get_tokens, IsCurator
from ...REST import user_throttles

"""
A view class for registering new users
"""
class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [user_throttles.anonStricter]
    serializer_class = RegisterSerializer

    def post(self, request):
        unverified_user = request.data
        serializer = self.serializer_class(data=unverified_user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        real_user = CustomUser.objects.get(email=serializer.data['email'])

        new_token = get_tokens(real_user)['access']

        context = {
            'request': request,
            'protocol': request.scheme,

            # for unit tests:
            'domain': "harmless_domain_name",

            # for production:
            #'domain': request.META['HTTP_HOST'],
            'username': real_user.username,
            'token': str(new_token)
        }

        email = EmailMessage(
            'registration',
            render_to_string('register_email.txt', context),
            'collectr2021@outlook.com', # FROM
            [real_user.email], # TO
        )
        email.send(fail_silently=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
A view class for setting user account active based on email registration link.
"""
class RegisterDoneView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [user_throttles.anonStrictest]
    serializer_class = RegisterDoneSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'well_done': 'Successfully activated!!!!'},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired, register faster next time.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token, don\'t edit the registration link please.'},
                            status=status.HTTP_400_BAD_REQUEST)

"""
A view class for logon.
"""
class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [user_throttles.anonRelaxed]
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

"""
A view class for logout.
"""
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = [user_throttles.userNormal]
    serializer_class = LogoutSerializer

    def post(self, request):
        # apparently no need to delete access token on logout, it should time out quickly enough anyway.
        # https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_204_NO_CONTENT)

"""
A view class for requesting a password reset email.
"""
class ResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [user_throttles.anonStricter]
    serializer_class = ResetSerializer

    def post(self, request):
        email = request.data.get('email', '')

        if CustomUser.objects.filter(email=email).exists():
            real_user = CustomUser.objects.get(email=email)
            #uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            new_token = get_tokens(real_user)['access']

            context = {
                'request': request,
                'protocol': request.scheme,
                # for unit tests:
                'domain': "harmless_domain_name",

                # for production:
                #'domain': request.META['HTTP_HOST'],
                'username': real_user.username,
                'token': str(new_token)
            }

            email = EmailMessage(
                'reset',
                render_to_string('reset_email.txt', context),
                'collectr2021@outlook.com',
                [real_user.email], # real_user.email or collectr2021@outlook.com
            )
            email.send(fail_silently=False)

        # not giving away email info to strangers, same msg for success/failure:
        return Response({'success': 'If you didn\'t stuff up your email, '
                                    'then we sent you a link to reset your password.'}, status=status.HTTP_200_OK)

"""
A view class for authenticating user based on email registration link.
"""
class ResetOKView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [user_throttles.anonStrictest]
    # validates reset link token is correct, authenticates user.
    # serializer is not used at all.
    serializer_class = ResetDoneSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            id=payload['user_id']
            user_from_token = CustomUser.objects.get(id=id)
            manual_auth_tokens = get_tokens(user_from_token)
            return Response(manual_auth_tokens, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Reset link expired, respond faster next time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token, don\'t edit the reset link please.'},
                            status=status.HTTP_400_BAD_REQUEST)

"""
A view class for resetting password for authenticated users.
"""
class ResetDoneView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [user_throttles.userNormal]
    serializer_class = ResetDoneSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data, user=self.request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.update_password()
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

"""
A view class for providing basic user info for internal use on the front end.
"""
class BasicUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [user_throttles.userNormal]

    def get(self, request):
        serializer = BasicUserSerializer(self.request.user)
        return Response(serializer.data)

"""
A view class for users to edit their profile.
"""
class EditUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [user_throttles.userNormal]
    serializer_class = EditUserSerializer

    def get_queryset(self):
        return CustomUser.objects.get(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        instance = CustomUser.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(instance, data=self.request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

"""
A view class for curators to recruit new curators.
"""
class PromoteView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCurator]
    throttle_classes = [user_throttles.userNormal]
    serializer_class = PromoteUserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)

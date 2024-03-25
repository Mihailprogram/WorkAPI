from rest_framework.response import Response
from .serializers import TokenSerializer, ComponentSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import viewsets
from .models import Component
from rest_framework import filters


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title_categories__icontains', )


class Email(APIView):
    def get(self, request, uid, token, *args, **kwargs):
        try:
            uid = str(urlsafe_base64_decode(uid), 'utf-8')
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            # Активируйте аккаунт пользователя
            user.is_active = True
            user.save()
            return Response({"message": "Ваш аккаунт успешно активирован."})
        else:
            return Response({"message": "Ошибка активации аккаунта."})
        

class RegistrationWithTokenView(APIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Проводим аутентификацию пользователя
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Генерируем токен
            token, _ = Token.objects.get_or_create(user=user)
            token_data = {
                'auth_token': str(token.key),
            }
            return Response(token_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Invalid credentials'}, 
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Просто удаляем токен пользователя
        token = Token.objects.get(user=request.user)

        # Удаляем токен
        token.delete()

        # Возвращаем успешный ответ
        return Response({'detail': 'Successfully logged out.'}, 
                        status=status.HTTP_200_OK)
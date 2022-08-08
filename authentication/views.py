from rest_framework import status
from .models import Account
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .serializers import AccountSerializer, LoginSerializer, UpdateAccountSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from django.utils.crypto import get_random_string


class AccountViewSet(APIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.filter(is_active=True)
    permission_classes = ()

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj = get_object_or_404(Account, pk=serializer.data["id"])
            pwd = get_random_string(length=10)
            obj.set_password(pwd)
            obj.save()
            print(pwd)
            return Response({'success', 'User created'}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        acc = get_object_or_404(Account, pk=pk)
        ser = UpdateAccountSerializer(acc, request.data, partial=True)
        ser.is_valid(raise_exception=True)
        acc = AccountSerializer(acc)
        ser.save()
        return Response(acc.data)

    def get(self, request, pk=None):
        queryset = Account.objects.filter(is_active=True)
        acc = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(acc)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        serializer = Account.objects.filter(is_active=True)
        acc = get_object_or_404(serializer, pk=pk)
        acc.is_active = False
        acc.save()
        return Response(200)


class UserLoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        serializer = self.serializer_class(data=request.data)
        user = get_object_or_404(Account, email=email, is_active=True)
        token, created = Token.objects.get_or_create(user=user)
        account = AccountSerializer(user).data

        data = {
            'token': token.key,
            'account': account,
        }

        return Response(data)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)

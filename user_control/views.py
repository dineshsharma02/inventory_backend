from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from .serializers import CreateUserSerializer,CustomUser,LoginUserSerializer,UpdatePasswordSerializer,CustomUserSerializer, UserActivitySerializer
from rest_framework import status
from rest_framework.response import Response
from inventory_api.utils import get_access_token
from inventory_api.custom_methods import IsAuthenticatedCustom
from .models import UserActivity
from rest_framework.authentication import authenticate
from django.db import IntegrityError


def add_user_activity(user,action):
    UserActivity.objects.create(
        user_id=user.id,
        email = user.email,
        fullname = user.fullname,
        action = action
    )

class CreateUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self,request):
        valid_request = self.serializer_class(data = request.data)
        valid_request.is_valid(raise_exception=True)
        try:
            CustomUser.objects.create(**valid_request.validated_data)
        except IntegrityError:
            # raise 
            # raise IntegrityError(Response({"data":{"error":"User Email Already Registered"}},status=status.HTTP_400_BAD_REQUEST))
            raise IntegrityError("Duplicate email found!!")

        add_user_activity(request.user,"Added new user")
        return Response({"Success":"User Created"},status=status.HTTP_200_OK)


class LoginUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginUserSerializer

    def create(self, request):
        valid_request = self.serializer_class(data = request.data)
        valid_request.is_valid(raise_exception=True)
        new_user = valid_request.validated_data["is_new_user"]
        if new_user:
            user = CustomUser.objects.filter( 
                email = valid_request.validated_data["email"]
            )

            if user:
                user = user[0]
                if not user.password:
                    return Response({"user_id":user.id})
                else:
                    raise Exception("User already has a password")
            else:
                raise Exception("User with this email not found!!!")


        user = authenticate(
            username = valid_request.validated_data["email"],
            password = valid_request.validated_data.get("password",None)
        )
        if not user:
            return Response({"error":"Invalid email or password"},status = status.HTTP_400_BAD_REQUEST)

        access = get_access_token({"user_id":user.id},1)
        user.last_login = datetime.now()
        user.save()
        add_user_activity(user,"Logged in")
        return Response({"Access":access})

class UpdatePaasswordView(ModelViewSet):
    serializer_class = UpdatePasswordSerializer
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()

    def create(self,request):
        valid_request = self.serializer_class(data = request.data)
        valid_request.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(id = valid_request.validated_data["user_id"])
        if not user:
            raise Exception("User with id not found")

        user = user[0]
        user.set_password(valid_request.validated_data["password"])
        user.save()
        add_user_activity(user,"Password Updated")
        return Response({"success":"Password set successfully"})

class MeView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom,)

    def list(self,request):
        data = self.serializer_class(request.user).data
        return Response(data)



class UserActivityView(ModelViewSet):
    serializer_class = UserActivitySerializer
    http_method_names = ["get"]
    queryset = UserActivity.objects.all()
    permission_classes = (IsAuthenticatedCustom,)


class UsersView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["get"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom,)

    def list(self,request):
        users = self.queryset.filter(is_superuser=False)
        data = self.serializer_class(users,many=True).data
        return Response(data)
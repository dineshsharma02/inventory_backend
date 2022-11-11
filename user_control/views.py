from rest_framework.viewsets import ModelViewSet
import datetime
from .serializers import CreateUserSerializer,CustomUser,LoginUserSerializer
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authentication import authenticate

class CreateUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

    def create(self,request):
        valid_request = self.serializer_class(data = request.data)
        valid_request.is_valid(raise_exception=True)
        CustomUser.objects.create(**valid_request.validated_data)

        return Response({"Success":"User Created"}, staus=status.HTTP_201_CREATED)


class LoginUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginUserSerializer

    def create(self, request):
        valid_request = self.serializer_class(data = request.data)
        valid_request.is_valid(raise_exception=True)
        new_user = valid_request.validated_data("is_new_user")
        if new_user:
            user = CustomUser.objects.filter( 
                valid_request.validated_data["email"]
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
            password = valid_request.validated_data("password",None)
        )
        if not user:
            return Response({"error":"Invalid email or password"},status = status.HTTP_400_BAD_REQUEST)

        access = get_access_token({"user_id":user.id},1)
        user.last_login = datetime.now()
        user.save()
        return Response({"Access":access})


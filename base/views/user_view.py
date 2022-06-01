from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import *
from django.contrib.auth.models import User
from base.serializer import UserSerializer, UserSerializerwithToken
# Create your views here.
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['email'] = user.username
    #     token['message'] = "Hello World"

    #     # ...

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # refersh = self.get_token(self.user)

        # data['refersh'] = str(refersh)
        # data['access'] = str(refersh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)
        # data['username'] = self.user.username
        # data['email'] = self.user.email

        serializer = UserSerializerwithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(requests):
    # return JsonResponse("Hello",safe=False)
    return Response("Hello")


@api_view(['POST'])
def registerUser(req):
    data = req.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerwithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with mail already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(req):
    user = req.user
    serializer = UserSerializerwithToken(user, many=False)
    data = req.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
        
    user.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(req):
    user = req.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(req):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsersById(req,pk):
    print("called getUsersById>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUserProfileByAdmin(req,pk):
    user = User.objects.get(id=pk)
    data = req.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    
        
    user.save()
    serializer = UserSerializerwithToken(user, many=False)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def deleteUser(req,pk):

    userforDeletion= User.objects.get(id=pk)

    userforDeletion.delete()

    return Response("User was deleted")

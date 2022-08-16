from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import DepartmentSerializer, DesignationSerializer, ProfileSerializer, LoginSerializer, ProjectSerializer, UserProfileSerializer, UserSerializer
from django.contrib import auth
from rest_framework.authtoken.models import Token 
from .models import Profile
from django.contrib.auth.models import User


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    def post(self, request):
        user = request.data
        #print("This is user",user)
        #user['username'] = user['email']
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializers= self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        user_data = request.data
        userx = auth.authenticate(username=user_data['username'], password=user_data['password'])
        return Response(LoginSerializer.generateToken(self, userx),status=status.HTTP_200_OK)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    #print(request.META['HTTP_AUTHORIZATION'])
    pre_token = request.META['HTTP_AUTHORIZATION']
    print(pre_token)
    pre_token = pre_token[6:]
    print(pre_token)
    pk = Token.objects.get(key=pre_token)
    print('PRIMARY KEY________>>>>',pk.user_id)
    snippet = User.objects.get(id=pk.user_id)
    
    profile_instance = Profile.objects.get(user=snippet)
    serializers = UserProfileSerializer(profile_instance)
    return Response(serializers.data, status=status.HTTP_200_OK)

'''
Needs : 
Authorization: Token xxxx
'''

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def logoutCall(request):
    #print(request.META['HTTP_AUTHORIZATION'])
    pre_token = request.META['HTTP_AUTHORIZATION']
    print(pre_token)
    pre_token = pre_token[6:]
    print(pre_token)
    pk = Token.objects.get(key=pre_token).delete()
    data = {
        "success": "Token deleted successfully"
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def getUserProfileOnId(request,pk):
    instance = Profile.objects.get(id=pk)
    serializers = UserProfileSerializer(instance)
    return Response(serializers.data)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def allUserProfile(request):
    qs = Profile.objects.all()
    print(qs)
    serializers = UserProfileSerializer(qs, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addDepartment(request):
    serializer_class = DepartmentSerializer
    serializers = serializer_class(data=request.data)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addDesignation(request):
    serializer_class = DesignationSerializer
    serializers = serializer_class(data=request.data)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addProjects(request):
    serializer_class = ProjectSerializer
    serializers = serializer_class(data=request.data)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(serializers.data, status=status.HTTP_200_OK)



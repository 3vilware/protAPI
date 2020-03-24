from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from protAPI.proteinnet import predict, train
from rest_framework import serializers, viewsets, generics, views, status
from protAPI.models import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from protMaster import settings
from django.core.files import File

def index(request):
    predict.init()
    #train.run_experiment()
    return HttpResponse("OK working")


def runJob(request):
    if request.method == 'POST':
        aa_chain = request.POST.get('chain')

        pdb_name = predict.run_job(aa_chain)

        data = {
            'pdb_name': pdb_name
        }

        return JsonResponse(data, safe=False)


# class Login(views.APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         token = Token.objects.get_or_create(user=request.user)
#
#         print(token)
#
#         data = {"token": token.key}
#         return Response(data)

class Register(views.APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                # serializer.data.update({"token":token.key})
                print("OK CREATED")
                return Response({"token":token.key}, status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors)


class TestEndpoint(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {"user": request.user.username}
        return Response(data)

class RunJob(views.APIView):
    permission_classes = (IsAuthenticated,)

    # base_dir = settings.BASE_DIR + "/protAPI/proteinnet/"
    def post(self, request):
        aa_chain = request.data['chain']

        job = Job(user=request.user)
        job.save()
        pdb_name = predict.run_job(aa_chain, job_id=job.pk)
        job.pdb = pdb_name
        job.save()

        data = {
            'pdb_name': pdb_name,
            'job_id': job.pk
        }

        return Response(data)



"""
START serillizers
"""
class ProtUserSerilizer(serializers.ModelSerializer):
    # jobs = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['name', 'jobs', 'id']
        read_only_fields = ['jobs']


class JobSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name')
        write_only_fields = ['password']

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=4)
    first_name = serializers.CharField(min_length=3)


    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
             password=validated_data['password'], first_name=validated_data['first_name'])
        return user


"""
END Serilizers
"""

class UserViewSetAll(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProtUserSerilizer

class JobViewSetAll(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobSerilizer

class UserViewSet(views.APIView):

    def get(self, request, pk):
        todo = User.objects.get(pk=pk)
        serializer = ProtUserSerilizer(todo)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = User(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = User.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        print(request.data.get('name'))
        product = User.objects.get(pk=pk)
        serializer = ProtUserSerilizer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






def viewProt(request, name):
    print(name)

    context = {"name":name}
    return render(request, 'view_prot.html', context)
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
from django.db.models import Q
import requests
from protAPI import cloud_storage
from django.views.decorators.csrf import csrf_exempt
import json
import os
from protAPI.scripts import run_training
try:
    from protAPI.proteinnet.preprocessing import *
    from protAPI.proteinnet.models import *
    from protAPI.proteinnet.training import train_model
except:
    print("Import error")
    from preprocessing import *
    from models import *
    from training import train_model



def index(request):
    print("LOADING FUCKING MODEL")
    def run_experiment():
        # pre-process data
        process_raw_data(False, force_pre_processing_overwrite=False)

        # run experiment
        # training_file = args.input_file
        training_file = settings.BASE_DIR + "/protAPI/proteinnet/data/preprocessed/sample.txt.hdf5"
        validation_file = settings.BASE_DIR + "/protAPI/proteinnet/data/preprocessed/sample.txt.hdf5"
        # validation_file = args.input_file

        model = MyModel(21, 5, use_gpu=False)  # embed size = 21

        train_loader = contruct_dataloader_from_disk(training_file, 5)
        validation_loader = contruct_dataloader_from_disk(validation_file, 5)

        train_model_path = train_model(data_set_identifier="TRAINXX",
                                       model=model,
                                       train_loader=train_loader,
                                       validation_loader=validation_loader,
                                       learning_rate=0.1,
                                       minibatch_size=5,
                                       eval_interval=5,
                                       hide_ui=True,
                                       use_gpu=False,
                                       minimum_updates=1) # Epochs

        print("Completed training, trained model stored at:")
        print(train_model_path)
    run_experiment()
    return HttpResponse("OK working")


@csrf_exempt
def generateModel(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body["code"])

        file_path = settings.BASE_DIR + "/protApi/proteinnet/custom_models.py"
        f = open(file_path, "a")
        f.write(body["code"])
        f.close()

        return JsonResponse("")




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


class GenerateModel(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ModelStructureSerilizer(data=request.data)
        if serializer.is_valid():
            model_structure = serializer.save()
            file_path = settings.BASE_DIR + "/protApi/proteinnet/custom_models.py"
            f = open(file_path, "a")
            f.write(model_structure.code)
            f.close()

            data = {
                "message": "success"
            }
            print("Model OK")
            run_training(model_structure.name, model_structure.epochs)

            return Response(data)
        else:
            data = {
                "message": "error"
            }
            return Response(data)


class RunJob(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        aa_chain = request.data['chain']
        print("VAL", aa_chain)
        try:
            model = request.data['model']
        except:
            model = ""

        try:
            model = ModelTrained.objects.get(Q(author=request.user) | Q(public=True), pk=model)
        except:
            model = ""
        if model:
            job = Job(user=request.user, model=model)
        else:
            job = Job(user=request.user)

        job.save()
        pdb_name = predict.run_job(aa_chain, job_id=job.pk, model=model)
        job.pdb = pdb_name
        job.save()

        data = {
            'pdb_name': pdb_name,
            'job_id': job.pk
        }

        return Response(data)

    def get(self, request):
        todo = Job.objects.filter(user=request.user).order_by('-date')
        serializer = JobSerilizer(todo, many=True)
        return Response(serializer.data)




"""
START serillizers
"""
class ProtUserSerilizer(serializers.ModelSerializer):
    # jobs = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id']
        read_only_fields = ['jobs']


class JobSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ModelTrainedSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ModelTrained
        fields = '__all__'
        read_only_fields = ['author']

class ModelStructureSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ModelStructure
        fields = '__all__'
        read_only_fields = ['author']



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




class ModeltrainedViewSet(generics.ListCreateAPIView): # Create and read models for a user
    permission_classes = (IsAuthenticated,)
    queryset = ModelTrained.objects.all()
    serializer_class = ModelTrainedSerilizer

    def list(self, request):
        queryset = ModelTrained.objects.filter(author=request.user)
        serializer = ModelTrainedSerilizer(queryset, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ModelTrainedChange(views.APIView):

    def delete(self, request, pk, format=None):
        model = ModelTrained.objects.get(pk=pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):

        model = ModelTrained.objects.get(pk=pk)
        serializer = ModelTrainedSerilizer(model, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        todo = ModelTrained.objects.filter(public=True)
        serializer = ModelTrainedSerilizer(todo, many=True)
        return Response(serializer.data)





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
        # print(request.data.get('name'))
        product = User.objects.get(pk=pk)
        serializer = ProtUserSerilizer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProteinData(views.APIView):

    def get(self, request, protein_id):
        structure = get_pdb(protein_id)
        path = settings.MEDIA_ROOT + "/" + protein_id+".pdb"
        f = open(path, "w")
        f.write(structure)
        f.close()

        fasta = get_fasta(protein_id)

        data = {
            "response":"success",
            "pdb": protein_id+".pdb",
            "fasta": fasta,
        }
        return Response(data)



def viewProt(request, name):
    print(name)
    try:
        with open("media/" + name) as f:
            f.read()
            f.close()
    except IOError:
        print("No file in local server")
        cloud_storage.download_file(os.path.join(settings.MEDIA_ROOT, name), name)

    context = {"name":name}
    return render(request, 'view_prot.html', context)



def get_pdb(pdb_id):
    result = requests.get(
            'https://files.rcsb.org/view/{}.pdb'.format(pdb_id))

    #print(result.text)
    return result.text


def get_fasta(pdb_id):
    begin = False
    full_sequence = ""
    result = requests.get(
            'https://www.rcsb.org/fasta/entry/{}/display'.format(pdb_id))
    for line in str(result.text).splitlines():
        if line.startswith('>') and not begin:
            begin = True
        elif line.startswith('>') and begin:
            break
        else:
            full_sequence = full_sequence + line
    #print(list(full_sequence)) # tolist
    return full_sequence
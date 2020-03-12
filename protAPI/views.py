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

"""
START serillizers
"""
class ProtUserSerilizer(serializers.ModelSerializer):
    jobs = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProtUser
        fields = ['name', 'jobs', 'id']
        read_only_fields = ['jobs']


class JobSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


"""
END Serilizers
"""

class UserViewSetAll(generics.ListCreateAPIView):
    queryset = ProtUser.objects.all()
    serializer_class = ProtUserSerilizer

class JobViewSetAll(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobSerilizer

class UserViewSet(views.APIView):

    def get(self, request, pk):
        todo = ProtUser.objects.get(pk=pk)
        serializer = ProtUserSerilizer(todo)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProtUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = ProtUser.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        print(request.data.get('name'))
        product = ProtUser.objects.get(pk=pk)
        serializer = ProtUserSerilizer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






def viewProt(request, name):
    print(name)

    context = {"name":name}
    return render(request, 'view_prot.html', context)
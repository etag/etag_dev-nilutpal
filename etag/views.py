from django.shortcuts import render
from rest_framework.authtoken.models import Token
#from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.renderers import BrowsableAPIRenderer, JSONPRenderer,JSONRenderer,XMLRenderer,YAMLRenderer #, filters
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
#from renderer import CustomBrowsableAPIRenderer
from filters import ReadersFilter,ReaderLocationFilter, TagReadsFilter,TagsFilter, AnimalFilter
from etag.models import Readers, TagAnimal, ReaderLocation,Tags,TagReads,AccessoryData
from serializer import ReaderSerializer, AnimalSerializer,ReaderLocationSerializer,TagsSerializer,TagReadsSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import os, requests,json
#import DjangoModelPermissionsOrAnonReadOnly


class ReadersViewSet(viewsets.ModelViewSet):
    """
    RFID Readers table view set.
    """
    model = Readers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReadersFilter
    search_fields = ('name', 'description',)
    ordering_fields =  '__all__'
    ordering_fields = '__all__'
    
    def get_queryset(self):
        user = self.request.user
        if not user:
            return []	
        return Readers.objects.filter(user_id=user.id)

    def create(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            reader = Readers.objects.create(reader_id=serializer.data['reader_id'],name=serializer.data['name'],description=serializer.data['description'])
            reader.user_id = self.request.user.id
            reader.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReaderLocationViewSet(viewsets.ModelViewSet):
    """
    Reader Location table view set.
    """
    model = ReaderLocation
    queryset = ReaderLocation.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReaderLocationSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReaderLocationFilter
    search_fields = ('name', 'latitude','longitude','start_timestamp','end_timestamp')
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
        if not user:
            return []
             
        return ReaderLocation.objects.filter(reader__user_id = user.id)

	
class AnimalViewSet(viewsets.ModelViewSet):
    """
    Animal table view set.
    """
    model = TagAnimal
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AnimalSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = AnimalFilter
    ordering_fields = ('name', 'description', 'end_timestamp', 'start_timestamp')
	
    def get_queryset(self):
        user = self.request.user
        if not user:
            return []
             
        return TagAnimal.objects.filter(tag__user_id = user.id)

	
class TagsViewSet(viewsets.ModelViewSet):
    """
    Tags table view set.
    """
    model = Tags
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter ,filters.OrderingFilter)
    filter_class = TagsFilter
    search_fields = ('tag_id',)
    ordering_fields = '__all__'
	
    def get_queryset(self):
        user = self.request.user
        if not user:
            return []
        return Tags.objects.filter(user_id=user.id)
		
    def create(self, request):
        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            reader = Tags.objects.create(tag_id=serializer.data['tag_id'],name=serializer.data['name'],description=serializer.data['description'])
            reader.user_id = self.request.user.id
            reader.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class TagReadsViewSet(viewsets.ModelViewSet):
    """
    TagReads table view set.
    """
    model = TagReads
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagReadsSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,JSONPRenderer,XMLRenderer,YAMLRenderer)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = TagReadsFilter
    search_fields = ('tag_id',)
    ordering_fields =  '__all__' 
	
    def get_queryset(self):
        user = self.request.user
        if not user:
            return []
             
        return TagReads.objects.filter(tag__user_id = user.id)
	
class AccessoryDataViewSet(viewsets.ModelViewSet):
    """
    AccessoryData table view set.
    """
    model=AccessoryData
    queryset = AccessoryData.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, YAMLRenderer)
    search_fields = ('accessory_type', 'value')


class etagDataUploadView(APIView):
        permission_classes =(IsAuthenticated,)
        #parser_classes = (MultiPartParser, FormParser,FileUploadParser,)
        parser_classes = (FileUploadParser,)
        renderer_classes = (JSONRenderer,)

        def post(self, request, uploadDirectory="/data/file_upload",format=None):
                #Get Token for task submission
                tok = Token.objects.get_or_create(user=self.request.user)
                headers = {'Authorization':'Token {0}'.format(str(tok[0])),'Content-Type':'application/json'} 
                #check if uploadDirectory exists
                if not os.path.isdir(uploadDirectory):
                    os.makedirs(uploadDirectory)
                result={} #'var':dir(request),'fpath':request.build_absolute_uri().split('/')}
                local_file=""
                reader_id = request.DATA.get("reader_id")
                for key,value in request.FILES.iteritems():
                        filename= value.name
                        local_file = "%s/%s" % (uploadDirectory,filename)
                        self.handle_file_upload(request.FILES[key],local_file)
                        result[key]=local_file
                #Request task
                task_name = "etagq.tasks.tasks.etagDataUpload"
                payload={"function": task_name,"queue": "celery","args":[reader_id,local_file,str(tok[0])],"kwargs":{},"tags":[]}
                components = request.build_absolute_uri().split('/')
                hostname = os.environ.get("host_hostname", components[2])
                r=requests.post("{0}//{1}/api/queue/run/etagq.tasks.tasks.etagDataUpload/.json".format(components[0],hostname),data=json.dumps(payload),headers=headers)
                return Response(r.json())


        def handle_file_upload(self,f,filename):
                if f.multiple_chunks():
                        with open(filename, 'wb+') as temp_file:
                                for chunk in f.chunks():
                                        temp_file.write(chunk)
                else:
                        with open(filename, 'wb+') as temp_file:
                                temp_file.write(f.read())

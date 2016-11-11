__author__ = 'mstacy'
import django_filters

from models import Readers, ReaderLocation,Tags, TagReads, TagAnimal


class ReadersFilter(django_filters.FilterSet):
    reader_id = django_filters.CharFilter(lookup_type='iexact')
    #name = django_filters.CharFilter(lookup_type='iexact')
    #description = django_filters.CharFilter(lookup_type='iexact')
    #user_id = django_filters.CharFilter(lookup_type='iexact')
    
    class Meta:
        model = Readers
        fields = ['reader_id',]
        #fields = ['reader_id', 'name', 'description', 'user_id',]
		

class ReaderLocationFilter(django_filters.FilterSet):
    reader = django_filters.CharFilter(name='reader__reader_id' ,lookup_type='icontains')
    min_lat = django_filters.NumberFilter(name='latitude',lookup_type='gte')
    max_lat = django_filters.NumberFilter(name='latitude',lookup_type='lte')
    min_long = django_filters.NumberFilter(name='longitude',lookup_type='gte')
    max_long = django_filters.NumberFilter(name='longitude',lookup_type='lte')
    min_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='gte')
    max_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='lte')
    min_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='gte')
    max_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='lte')
    
    class Meta:
        model = ReaderLocation
        fields = ['reader', 'latitude','longitude','start_timestamp','end_timestamp']

        
class TagsFilter(django_filters.FilterSet):
    tag_id = django_filters.CharFilter(lookup_type='iexact')
    #name = django_filters.CharFilter(lookup_type='icontains')
    #description = django_filters.CharFilter(lookup_type='icontains')
    
    class Meta:
        model = Tags
        fields = ['tag_id',]
        #fields = ['tag_id', 'name','description']

        
class TagReadsFilter(django_filters.FilterSet):
    reader = django_filters.CharFilter(name='reader__reader_id' ,lookup_type='icontains')
    tag = django_filters.CharFilter(name='tag__tag_id' ,lookup_type='icontains')
    min_timestamp = django_filters.DateTimeFilter(name='tag_timestamp', lookup_type='gte')
    max_timestamp = django_filters.DateTimeFilter(name='tag_timestamp', lookup_type='lte')
    
    class Meta:
        model = TagReads
        fields = ['tag','reader']
       

class AnimalFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(name='tag__tag_id' ,lookup_type='icontains')
    name = django_filters.CharFilter(name='name',lookup_type='icontains')
    description = django_filters.CharFilter(name='description',lookup_type='icontains')
    min_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='gte')
    max_start_timestamp = django_filters.DateTimeFilter(name='start_timestamp', lookup_type='lte')
    min_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='gte')
    max_end_timestamp = django_filters.DateTimeFilter(name='end_timestamp', lookup_type='lte')

    class Meta:
        model = TagAnimal
        fields = ['tag','name','description','start_timestamp', 'end_timestamp']

    

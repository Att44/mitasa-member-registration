import django_filters 
from .models import *
from django_filters import DateFilter

class MemberFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="data_created", lookup_expr='gte')
    end_date = DateFilter(field_name="data_created", lookup_expr='lte')
    class Meta:
        model = Member
        fields = ['nama']
        exclude = ['data_created']

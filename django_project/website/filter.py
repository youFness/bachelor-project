import django_filters
from job.models import Job

class Jobfilter(django_filters.FilterSet):
    # to search just for keey words
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model= Job
        fields=['title','state','job_type','industry']

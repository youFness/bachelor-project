from django.shortcuts import render
from job.models import Job, ApplyJob
from .filter import Jobfilter



def home(request):
    filter = Jobfilter(request.GET,queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter':filter}
    return render(request,'website/home.html',context)



def job_listing(request):
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    context={'jobs':jobs}
    return render(request,'website/job_listing.html',context)



# def job_details(request, pk):
#     job = Job.objects.get(id=pk)
#     related_jobs = Job.objects.filter(title__icontains=job.title).exclude(id=job.id)[:1]
    
#     if ApplyJob.objects.filter(user=request.user, job=job).exists():
#         has_applied = True
#     else:
#         has_applied = False
    
#     context = {
#         'job': job,
#         'related_jobs': related_jobs,
#         'has_applied': has_applied,
#     }
    
#     return render(request, 'website/job_details.html', context)

# views.py
import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import ApplyJob, Job
from .form import CreateJobForm, UpdateJobForm
from django.core.mail import send_mail
from users.models import User
from django.urls import reverse





def create_job(request):
    if request.user.is_recruiter and request.user.has_company:
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.user = request.user
                job.company = request.user.company
                job.state = form.cleaned_data['state']
                job.save()
                messages.info(request, 'New job has been posted')
                send_job_alerts(job)  # Send job alert to matching applicants
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
                return redirect('create-job')
        else:
            form = CreateJobForm()
            context = {'form': form}
            return render(request, 'job/create_job.html', context)
    else:
        messages.warning(request, 'Permission denied')
        return redirect('dashboard')

# Function to send job alerts



# def send_job_alerts(new_job):
#     # Retrieve the email addresses of matching applicants
#     matching_applicants = User.objects.filter(resume__job_title=new_job.title)
#     email_recipients = matching_applicants.values_list('email', flat=True)

#     # Print the matching applicants and email recipients for debugging
#     print("Matching Applicants:", matching_applicants)
#     print("Email Recipients:", email_recipients)

#     # Build the job URL
#     job_url = reverse('job-details', args=[new_job.id])  # Assuming you have a URL pattern named 'job-detail'

#     # Create the job alert email
#     subject = 'New Job Alert: ' + new_job.title
#     message = f"Dear applicant, a new job has been posted matching your skills and preferences. " \
#               f"You can view the job details here: {job_url}"

#     # Send job alert email
#     send_mail(subject, message, 'djangojob1@gmail.com', email_recipients)
    




def send_job_alerts(new_job):
    # Retrieve the email addresses of matching applicants
    matching_applicants = User.objects.filter(resume__job_title=new_job.title)
    email_recipients = matching_applicants.values_list('email', flat=True)

    # Print the matching applicants and email recipients for debugging
    print("Matching Applicants:", matching_applicants)
    print("Email Recipients:", email_recipients)

    # Build the job URL
    job_url = reverse('job-details', args=[new_job.id])  # Assuming you have a URL pattern named 'job-details'
    job_listing_url = reverse('job-listing')  # Assuming you have a URL pattern named 'job-listing'

    # Create the job alert email
    subject = 'CareerHub: New Job Alert: ' + new_job.title

    # Build the email message
    message = f"Subject: {subject}\n\n"
    message += f"Dear applicant,\n\n"
    message += f"We are excited to inform you about a new job opportunity that matches your skills and preferences. "
    message += f"You can view the job details and apply through the following link:\n"
    message += f"{job_url}\n\n"
    message += f"Please find below the details of the job:\n\n"
    message += f"Industry: {new_job.industry}\n"
    message += f"Company: {new_job.company}\n"
    message += f"Salary: {new_job.salary}\n"
    message += f"State/City: {new_job.state},{new_job.city}\n"
    message += f"Job Description: {new_job.description}\n\n"
    message += f"If you would like to explore more job opportunities, you can view our job listing by clicking the button below:\n"
    message += f"[Show All Jobs]({job_listing_url})\n\n"
    message += f"Thank you for considering this opportunity.\n\n"
    message += f"Best regards,\n"
    message += f"CareerHub Team\n"
    message += f"Contact Information: djangojob1@gmail.com\n\n"

    # Send job alert email
    send_mail(subject, message, 'djangojob1@gmail.com', email_recipients)

#update job
def update_job(request, pk):
    job=Job.objects.get(pk=pk)
    if request.method=='POST':
        form = UpdateJobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.info(request,'your job informations is updated')
            return redirect('dashboard')
        else:
            messages.warning(request,'Something went wrong')
    else:
        form=UpdateJobForm(instance=job)
        context={'form':form}
        return render (request,'job/update_job.html',context)


def manage_jobs(request):
    jobs =Job.objects.filter(user=request.user,company=request.user.company)
    context={'jobs':jobs}
    return render(request,'job/manage_jobs.html',context)


# Function to send job application email
def send_job_application_email(applicant_email, job_title):
    subject = 'Job Application'
    message = f"Subject: {subject}\n\n"
    message += f"Dear applicant,\n\n"
    message += f"Thank you for applying for the role of {job_title}. Your application has been submitted successfully.\n\n"
    message += f"We appreciate your interest in the position and your application will be carefully reviewed. If your qualifications and experience match the requirements, the hiring company or organization will contact you for further steps in the hiring process.\n\n"
    message += f"Should you have any questions or require additional information, please feel free to contact us at info@careerhub.com.\n\n"
    message += f"Best regards,\n"
    message += f"CareerHub Team\n"
    message += f"Contact Information: djangojob1@gmail.com\n\n"

    from_email = 'djangojob1@gmail.com'
    recipient_list = [applicant_email]
    send_mail(subject, message, from_email, recipient_list)

    

def apply_to_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        job = Job.objects.get(pk=pk)
        if ApplyJob.objects.filter(user=request.user, job=job).exists():
            messages.warning(request, 'You have already applied for this job')
            return redirect('job-details', job_id=job.id)
        else:
            ApplyJob.objects.create(
                job=job,
                user=request.user,
                status='Pending'
            )

            # Send job application email
            applicant_email = request.user.email
            job_title = job.title
            send_job_application_email(applicant_email, job_title)

            messages.info(request, 'You have successfully applied for this job!')
            return redirect('job-listing')
    else:
        messages.info(request, 'Please log in to continue')
        return redirect('login')



def all_applicants(request, pk):
    job=Job.objects.get(pk=pk)
    applicants=job.applyjob_set.all()
    context={'job':job,'applicants':applicants}
    return render(request,'job/all_applicants.html',context)


def applied_jobs(request):
    jobs=ApplyJob.objects.filter(user=request.user)
    context={'jobs':jobs}
    return render(request,'job/applied_job.html',context)


#modify job
def update_job(request, pk):
    job = Job.objects.get(pk=pk)

    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'The job has been modified successfully.')
            return redirect('update-job', pk=pk)
        else:
            messages.error(request, 'Failed to modify the job. Please correct the errors in the form.')
    else:
        form = UpdateJobForm(instance=job)

    context = {'form': form, 'job': job}
    return render(request, 'job/create_job.html', context)



#to delete a job
def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.delete()
        return redirect('manage-jobs')  # Redirect to the job list page after successful deletion
    except Job.DoesNotExist:
        return render(request, 'job_not_found.html')  # Render a template for job not found error
    

def job_details(request, pk):
    job = Job.objects.get(id=pk)
    related_jobs = Job.objects.filter(title__icontains=job.title).exclude(id=job.id)[:1]
    
    if ApplyJob.objects.filter(user=request.user, job=job).exists():
        has_applied = True
    else:
        has_applied = False
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
        'has_applied': has_applied,
    }
    
    return render(request, 'website/job_details.html', context)

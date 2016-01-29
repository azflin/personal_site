from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


from forms import JobAnalysisForm
from scripts.job_scraper import get_jobs_analysis


def index(request):
    if request.method == 'POST':
        form = JobAnalysisForm(request.POST)
        if form.is_valid():
            if not request.POST.get('max_jobs'):
                results = get_jobs_analysis(
                    request.POST.get('search_query'),
                    request.POST.get('location'),
                    request.POST.get('country')
                )
            else:  # max_jobs non empty
                results = get_jobs_analysis(
                    request.POST.get('search_query'),
                    request.POST.get('location'),
                    request.POST.get('country'),
                    int(request.POST.get('max_jobs'))
                )
            return render(request, 'job_analysis/index.html', {'form': form, 'results': results})
        else:
            return render(request, 'job_analysis/index.html', {'form': form})
    else:
        form = JobAnalysisForm()
        return render(request, 'job_analysis/index.html', {'form': form})
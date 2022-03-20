from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
import work.models as mdl
from work.forms import CompanyForm, VacancyForm, ApplicationForm, ResumeForm
from datetime import date
from random import random
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Не смог придумать, как вывести количество вакансий по компаниям
# и специальностям на главной странице


def main_view(request):
    specialities = mdl.Specialty.objects.all()
    companies = sorted(mdl.Company.objects.all(), key=lambda x: random())[:8]
    return render(request, "work/index.html", context={
        "specialities": specialities,
        "companies": companies,
    })


def company_view(request, identificator):
    try:
        company = mdl.Company.objects.get(id=identificator)
    except mdl.Company.DoesNotExist:
        raise Http404
    vac_of_comp = mdl.Vacancy.objects.filter(company__id=identificator)
    return render(request, "work/company.html", context={
        "company": company,
        "vacancies": vac_of_comp,
        "count": len(vac_of_comp),
     })


def vacancy_view(request, identificator):
    try:
        vacancy = mdl.Vacancy.objects.get(id=identificator)
    except mdl.Vacancy.DoesNotExist:
        raise Http404
    return render(request, "work/vacancy.html", context={
        "vacancy": vacancy,
     })


@login_required
def vacancy_send_view(request, identificator):
    if request.method == 'POST':
        form = ApplicationForm(request.POST or None)
        try:
            vacancy = mdl.Vacancy.objects.get(id=identificator)
        except mdl.Vacancy.DoesNotExist:
            raise Http404
        if form.is_valid():
            form_s = form.save(commit=False)
            form_s.vacancy = vacancy
            form_s.user = request.user
            form_s.save()
            return redirect('main')
    else:
        form = ApplicationForm()
    return render(request, "work/vacancy-send.html", context={
        'form': form,
    })


def list_vacancies_view(request):
    vacancies = mdl.Vacancy.objects.all()
    return render(request, "work/vacancies.html", context={
        "vacancies": vacancies,
        "count": len(vacancies),
    })


def vacancy_cat_view(request, category):
    try:
        spec = mdl.Specialty.objects.get(code=category)
    except mdl.Specialty.DoesNotExist:
        raise Http404
    vacancies = mdl.Vacancy.objects.filter(speciality=spec.id)
    return render(request, "work/vacancy_cat.html", context={
        "spec": spec,
        "vacancies": vacancies,
        "count": len(vacancies),
    })


@login_required
def company_create(request):
    try:
        mdl.Company.objects.get(owner__id=request.user.id)
        return redirect('comp_edit')
    except mdl.Company.DoesNotExist:
        return render(request, "work/company-create.html")


@login_required
def company_edit(request):
    try:
        instance = mdl.Company.objects.get(owner__id=request.user.id)
    except mdl.Company.DoesNotExist:
        instance = {}
    if request.method == 'POST':
        form = CompanyForm(request.POST or None, request.FILES, instance=instance if instance else None)
        if form.is_valid():
            form_s = form.save(commit=False)
            form_s.owner = request.user
            form_s.save()
            return redirect('main')
    else:
        if not instance:
            form = CompanyForm()
        else:
            form = CompanyForm(initial={
                'name': instance.name,
                'logo': instance.logo,
                'location': instance.location,
                'employee_count': instance.employee_count,
                'description': instance.description,
            })
    return render(request, "work/company-edit.html", context={
        'form': form,
    })


@login_required
def mycomp_vacancy_list(request):
    try:
        mdl.Company.objects.get(owner__id=request.user.id)
    except mdl.Company.DoesNotExist:
        return redirect('comp_edit')
    vac_of_comp = mdl.Vacancy.objects.filter(company__owner__id=request.user.id)
    return render(request, "work/vacancy-list.html", context={
        'vacancies': vac_of_comp,
    })


@login_required
def mycomp_vacancy_create(request):
    try:
        mdl.Company.objects.get(owner__id=request.user.id)
    except mdl.Company.DoesNotExist:
        return redirect('comp_edit')
    if request.method == 'POST':
        comp = mdl.Company.objects.get(owner__id=request.user.id)
        form = VacancyForm(request.POST or None)
        if form.is_valid():
            form_s = form.save(commit=False)
            form_s.posted = date.today()
            form_s.company = comp
            if form_s.salary_min > form_s.salary_max:
                form_s.salary_min, form_s.salary_max = form_s.salary_max, form_s.salary_min
            form_s.save()
            return redirect('comp_vac')
    else:
        form = VacancyForm()
    return render(request, "work/vacancy_edit.html", context={
        'form': form,
    })


@login_required
def mycomp_vacancy_edit(request, identificator):
    try:
        instance = mdl.Vacancy.objects.get(id=identificator)
    except mdl.Vacancy.DoesNotExist:
        raise Http404
    if instance.company.owner.id != request.user.id:
        return redirect('comp_vac')
    vac_response = mdl.Application.objects.filter(vacancy__id=identificator)
    if request.method == 'POST':
        form = VacancyForm(request.POST or None, instance=instance)
        if form.is_valid():
            form_s = form.save(commit=False)
            if form_s.salary_min > form_s.salary_max:
                form_s.salary_min, form_s.salary_max = form_s.salary_max, form_s.salary_min
            form_s.save()
            return redirect('comp_vac')
    else:
        form = VacancyForm(initial={
            'title': instance.title,
            'speciality': instance.speciality,
            'salary_min': instance.salary_min,
            'salary_max': instance.salary_max,
            'skills': instance.skills,
            'description': instance.description,
        })
    return render(request, "work/vacancy_edit.html", context={
        "form": form,
        "responses": vac_response,
        "count_resp": len(vac_response),
    })


@login_required
def resume_create(request):
    try:
        mdl.Resume.objects.get(user__id=request.user.id)
        return redirect('res_edit')
    except mdl.Resume.DoesNotExist:
        return render(request, "work/resume-create.html")


@login_required
def resume_edit(request):
    try:
        instance = mdl.Resume.objects.get(user__id=request.user.id)
    except mdl.Resume.DoesNotExist:
        instance = {}

    if request.method == 'POST':
        form = ResumeForm(request.POST or None, instance=instance if instance else None)
        if form.is_valid():
            form_s = form.save(commit=False)
            form_s.user = request.user
            form_s.save()
            return redirect('main')
    else:
        if not instance:
            form = ResumeForm(initial={
                'name': request.user.first_name,
                'surname': request.user.last_name,
            })
        else:
            form = ResumeForm(initial={
                'name': instance.name,
                'surname': instance.surname,
                'status': instance.status,
                'salary': instance.salary,
                'specialty': instance.specialty,
                'grade': instance.grade,
                'education': instance.education,
                'experience': instance.experience,
                'portfolio': instance.portfolio,
            })
    return render(request, "work/resume-edit.html", context={
        'form': form,
    })


def search_view(request):
    s = request.GET.get('s')
    queryset = mdl.Vacancy.objects.filter(Q(title__icontains=s) | Q(skills__icontains=s) | Q(description__icontains=s))
    return render(request, "work/search.html", context={
        'vacancies': queryset,
        'count': len(queryset),
        'search': s,
    })


def custom404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404:</h1><h2>Данной страницы не существует</h2>')


def custom500(request):
    return HttpResponseServerError('<h1>Ошибка 500:</h1><h2>К сожалению, наш сервер сломался</h2>')

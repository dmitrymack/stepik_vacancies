from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render, redirect, get_object_or_404
import work.models as mdl
from work.forms import CompanyForm

# Не смог придумать, как вывести количество вакансий по компаниям
# и специальностям на главной странице


def main_view(request):
    specialities = mdl.Specialty.objects.all()
    companies = mdl.Company.objects.all()
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


def company_create(request):
    try:
        mdl.Company.objects.get(owner__id=request.user.id)
        return redirect('comp_edit')
    except mdl.Company.DoesNotExist:
        return render(request, "work/company-create.html")


def company_edit(request):
    try:
        instance = mdl.Company.objects.get(owner__id=request.user.id)
    except mdl.Company.DoesNotExist:
        instance = {}
    if request.method == 'POST':
        form = CompanyForm(request.POST or None, request.FILES, instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            return redirect('main')
    else:
        form = CompanyForm(initial={
            'name': instance.name,
            'logo': instance.logo,
            'location': instance.location,
            'employee_count': instance.employee_count,
            'description': instance.description
        })
    return render(request, "work/company-edit.html", context={
        'form': form,
    })


def custom404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404:</h1><h2>Данной страницы не существует</h2>')


def custom500(request):
    return HttpResponseServerError('<h1>Ошибка 500:</h1><h2>К сожалению, наш сервер сломался</h2>')

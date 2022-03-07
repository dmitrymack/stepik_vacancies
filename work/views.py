from django.shortcuts import render

def main_view(request):
    return render(request, "work/index.html")


def company_view(request, id):
    return render(request, "work/company.html")


def vacancy_view(request, id):
    return render(request, "work/vacancy.html")


def list_vacancies_view(request):
    return render(request, "work/vacancies.html")

def vacancy_cat_view(request, category):
    return render(request, "work/vacancy_cat.html")
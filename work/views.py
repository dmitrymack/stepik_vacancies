from django.http import HttpResponseNotFound, HttpResponseServerError
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


def custom404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404:</h1><h2>Данной страницы не существует</h2>')


def custom500(request):
    return HttpResponseServerError('<h1>Ошибка 500:</h1><h2>К сожалению, наш сервер сломался</h2>')

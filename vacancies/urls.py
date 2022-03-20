"""vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import work.views as view
import accounts.views as acc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.main_view, name='main'),
    path('company/<int:identificator>/', view.company_view, name='company'),
    path('vacancy/<int:identificator>/', view.vacancy_view, name='vacancy'),
    path('vacancy/<int:identificator>/send/', view.vacancy_send_view, name='vacancy_send'),
    path('vacancies/', view.list_vacancies_view, name='vacancies'),
    path('vacancies/cat/<str:category>/', view.vacancy_cat_view, name='vac_cat'),
    path('mycompany/letsstart/', view.company_create, name='comp_create'),
    path('mycompany/edit/', view.company_edit, name='comp_edit'),
    path('mycompany/vacancies/', view.mycomp_vacancy_list, name='comp_vac'),
    path('mycompany/vacancies/create/', view.mycomp_vacancy_create, name='comp_vac_cr'),
    path('mycompany/vacancies/<int:identificator>/', view.mycomp_vacancy_edit, name='comp_vac_ed'),
    path('resume/letsstart', view.resume_create, name='res_create'),
    path('resume/edit', view.resume_edit, name='res_edit'),
    path('search', view.search_view, name='search'),

    path('register', acc.SignUpView.as_view(), name='register'),
    path('login', acc.MyLoginView.as_view(), name='login'),
    path('logout', acc.logout_user, name='logout'),
]

handler404 = view.custom404
handler500 = view.custom500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

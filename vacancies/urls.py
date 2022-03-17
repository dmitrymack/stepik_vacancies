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
    path('vacancies/', view.list_vacancies_view, name='vacancies'),
    path('vacancies/cat/<str:category>/', view.vacancy_cat_view, name='vac_cat'),
    path('register', acc.SignUpView.as_view(), name='register'),
    path('login', acc.MyLoginView.as_view(), name='login'),
    path('logout', acc.logout_user, name='logout'),
]

handler404 = view.custom404
handler500 = view.custom500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

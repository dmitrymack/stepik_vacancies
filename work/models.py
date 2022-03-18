from django.contrib.auth.models import User
from django.db import models

from vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    logo = models.ImageField(default='https://place-hold.it/100x60', upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        pass


class Specialty(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    picture = models.ImageField(default='https://place-hold.it/100x60', upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=255)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    posted = models.DateField()

    def __str__(self):
        pass


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        pass
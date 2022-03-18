from django.core.management import BaseCommand
import work.models as mdl
import work.data as data


class Command(BaseCommand):

    def handle(self, *args, **options):
        # mdl.Company.objects.all().delete()
        # mdl.Specialty.objects.all().delete()
        # mdl.Vacancy.objects.all().delete()

        # for company in data.companies:
        #     mdl.Company.objects.create(
        #         name=company['title'],
        #         location=company['location'],
        #         logo=company['logo'],
        #         description=company['description'],
        #         employee_count=company['employee_count'],
        #     )
        for spec in data.specialties:
            mdl.Specialty.objects.create(
                code=spec['code'],
                title=spec['title'],
                picture = "static/specialties/specty_" + spec['code'] + '.png'
            )
        # for vac in data.jobs:
        #     mdl.Vacancy.objects.create(
        #         title=vac['title'],
        #         speciality=mdl.Specialty.objects.get(code=vac['specialty']),
        #         company=mdl.Company.objects.get(id=int(vac['company'])),
        #         skills=vac['skills'],
        #         description=vac['description'],
        #         salary_min=vac['salary_from'],
        #         salary_max=vac['salary_to'],
        #         posted=vac['posted'],
        #     )

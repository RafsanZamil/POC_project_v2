import os
from django.core.management.base import BaseCommand
from auths.models import CustomUser
import csv
from auths.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'users.csv')
        print("file:", file_path)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            created = 0
            skipped = 0
            for row in reader:
                email = (row['email'])
                username =(row['username'])
                is_active=(row['is_active'])
                is_superuser=(row['is_superuser'])
                password=(row['password'])

                csv_data={'email':email,'username':username,"password":password,}
                serializer=UserSerializer(data=csv_data)
                email_exists = CustomUser.objects.filter(email=email)
                username_exists = CustomUser.objects.filter(username=username)
                if email_exists or username_exists:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'This  {email} or {username} exists. Skipping.'))
                elif serializer.is_valid():

                    CustomUser.objects.create(
                        username=row['username'],
                        email=row['email'],
                        is_superuser=row['is_superuser'],
                        password=row['password'],
                        is_active=row['is_active'],
                    )
                    created += 1
                else:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'This  {email} or {username} has {serializer.errors}. Skipping.'))


            self.stdout.write(self.style.SUCCESS(f'Data imported successfully,created: {created}'))
            self.stdout.write(self.style.SUCCESS(f'Data importing skipped : {skipped}'))
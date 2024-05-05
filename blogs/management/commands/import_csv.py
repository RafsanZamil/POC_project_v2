import os

# myapp/management/commands/import_csv

from django.core.management.base import BaseCommand

from auths.models import CustomUser
from blogs.models import Post
import csv
class Command(BaseCommand):
    help = 'Imports data from a CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'posts.csv')
        print("file:", file_path)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            created = 0
            skipped = 0
            for row in reader:
                author_id = int(row['author'])
                try:
                    author = CustomUser.objects.get(id=author_id)
                except CustomUser.DoesNotExist:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'CustomUser with ID {author_id} does not exist. Skipping post.'))

                    continue
                Post.objects.create(
                    title=row['title'],
                    body=row['body'],
                    author=author,
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    is_active=row['is_active'],
                )
                created += 1

            self.stdout.write(self.style.SUCCESS(f'Data imported successfully,skipped : {skipped}'))

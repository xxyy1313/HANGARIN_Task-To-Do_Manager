from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Task, Note, SubTask, Category, Priority


class Command(BaseCommand):
    help = "Generate fake data for Task, Note, and SubTask"

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        if not categories or not priorities:
            self.stdout.write(self.style.ERROR(
                "Please add Category and Priority records first in admin."
            ))
            return

        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(20):
            naive_deadline = fake.date_time_this_month()
            aware_deadline = timezone.make_aware(naive_deadline)

            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=aware_deadline,
                status=fake.random_element(elements=statuses),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )

            for _ in range(random.randint(1, 3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

            for _ in range(random.randint(1, 4)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully."))
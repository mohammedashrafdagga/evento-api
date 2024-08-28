from django.core.management.base import BaseCommand
from apps.events.models import Category


class Command(BaseCommand):
    help = "Populate the Category model with example data"

    def handle(self, *args, **options):

        # Creating Parent Categories
        technology = Category.objects.get_or_create(name="Technology")[0]
        health = Category.objects.get_or_create(name="Health")[0]
        business = Category.objects.get_or_create(name="Business")[0]

        # Creating Subcategories for Technology
        Category.objects.get_or_create(
            name="Artificial Intelligence", parent=technology
        )
        Category.objects.get_or_create(name="Software Development", parent=technology)
        Category.objects.get_or_create(name="Cybersecurity", parent=technology)

        # Creating Subcategories for Health
        Category.objects.get_or_create(name="Mental Health", parent=health)
        Category.objects.get_or_create(name="Fitness", parent=health)
        Category.objects.get_or_create(name="Nutrition", parent=health)

        # Creating Subcategories for Business
        Category.objects.get_or_create(name="Entrepreneurship", parent=business)
        Category.objects.get_or_create(name="Marketing", parent=business)
        Category.objects.get_or_create(name="Finance", parent=business)

        self.stdout.write(self.style.SUCCESS("Successfully populated categories!"))

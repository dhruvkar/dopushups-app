from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.utils import Spreadsheet
from core.models import Challenger, Exercise, Column

class Command(BaseCommand):

    help = 'update column numbers for each challenger'


    def handle(self, *args, **kwargs):
        s = Spreadsheet()
        columns = s.columns_exercises()

        for col in columns:
            challenger = Challenger.objects.filter(name=col["name"]).first()
            exercise = Exercise.objects.filter(name=col["exercise"]).first()
            Column.objects.update_or_create(number=col["column"], challenger=challenger, exercise=exercise)
        return
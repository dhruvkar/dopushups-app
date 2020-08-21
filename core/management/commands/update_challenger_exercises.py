from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.utils import Spreadsheet
from core.models import Challenger, Exercise

class Command(BaseCommand):

    help = 'update column numbers for each challenger'


    def handle(self, *args, **kwargs):
    	s = Spreadsheet()
    	exercises = s.get_exercise_list()
    	ce = s.challenger_exercises()
    	for k, v in ce.items():
    		qs = []
    		for x in v:
    			qs.append(Exercise.objects.filter(name=x).first().id)

    		ch = Challenger.objects.update_or_create(name=k)
    		ch[0].exercises.add(*qs)
    		
    	
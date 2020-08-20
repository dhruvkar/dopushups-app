from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pendulum

class Spreadsheet:

    def __init__(self, key=settings.GOOGLE_SPREADSHEET_KEY, creds=settings.GOOGLE_CREDS_FILE):
        self.exercises = []
        self.challengers = []

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)
        gc = gspread.authorize(credentials)
        self.sheet = gc.open_by_key(key).sheet1
        self.get_exercise_list()

    def get_exercise_list(self):
        d = self.sheet.row_values(1)
        e = []
        for x in d:
            if not x.lower().startswith("date"):
                e.append(x.lower().split(' ')[-1])

        self.exercises = list(set(e))



    def get_challengers_from_spreadsheet(self):
        d = self.sheet.row_values(1)
        c = []
        for x in d:
            col = x.lower().split(' ')
            if not x.lower().startswith('date'):
                if len(col) == 2:
                    name = col[0]
                    c.append(name)
                elif len(col) == 3:
                    name = col[0] + "_" + col[1]
                    c.append(name)

        return c


class Command(BaseCommand):

    help = 'update column numbers for each challenger'


    def handle(self, *args, **kwargs):
    	s = Spreadsheet()
    	c = s.get_challengers_from_spreadsheet()
    	print (c)
    	
from django.conf import settings


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
        self.raw_header = self.sheet.row_values(1)
        
    def get_exercise_list(self):
        d = self.sheet.row_values(1)
        e = []
        for x in d:
            if not x.lower().startswith("date"):
                e.append(x.lower().split(' ')[-1])

        self.exercises = list(set(e))



    def get_challengers(self):
        c = []

        for x in self.raw_header:
            col = x.lower().split(' ')
            if not x.lower().startswith('date'):
                if len(col) == 2:
                    c.append(col[0])
                elif len(col) == 3:
                    name = col[0] + "_" + col[1]
                    c.append(name)
        
        return list(set(c))



    def challenger_exercises(self):
        challengers = self.get_challengers()
        d = {}
        for x in self.raw_header:
            header = x.lower().replace(' ', '_')
            if not header.startswith('date'):
                splith = header.split("_")
                if len(splith) == 2:
                    name = splith[0]
                elif len(splith) == 3:
                    name = splith[0] + "_" + splith[1]
                for c in challengers:
                    if c == name:
                        e = header.split("_")[-1]
                        if c in d:
                            d[c].append(e)
                        else:
                            d[c] = [e]

        return d

        

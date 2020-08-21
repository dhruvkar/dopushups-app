from django.conf import settings


import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pendulum



class Spreadsheet:

    def __init__(self, key=settings.GOOGLE_SPREADSHEET_KEY, creds=settings.GOOGLE_CREDS_FILE):

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)
        gc = gspread.authorize(credentials)
        self.wks = gc.open_by_key(key)
        self.sheet = self.wks.sheet1
        self.raw_header = self.sheet.row_values(1)
        

    def get_exercise_list(self):
        d = self.sheet.row_values(1)
        e = []
        for x in d:
            if not x.lower().startswith("date"):
                e.append(x.lower().split(' ')[-1])

        return list(set(e))



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

        

    def columns_exercises(self):
        #TODO - too many hits to the sheet, hits the quota limit. 
        # Need to find a bulk method of finding cells
        l = []
        ce = self.challenger_exercises()
        for k, v in ce.items():
            d = {}
            d['name'] = k
            search_name = ' '.join(k.split('_')).title()
            for x in v:
                search = search_name + " " + x.title() 
                cell = self.sheet.find(search)  #too many hits
                print (k, x)
                d['name'] = k
                d['exercise'] = x
                d['column'] = cell.col
            l.append(d)

        return l


    def get_range(self):
        cols = self.sheet.col_count
        rows = self.sheet.row_count
        ran = self.sheet.range('A1:{0}'.format(gspread.utils.rowcol_to_a1(rows, cols)))
        


    def get_today_row(self, timezone):
        pass


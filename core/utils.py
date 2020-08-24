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

    
    def parse_header_value(self, header):
        header = header.lower()
        if not header.startswith('date'):
            splith = header.split(" ")

            if len(splith) == 2:
                name = splith[0]
               
            elif len(splith) == 3:
                name = splith[0] + "_" + splith[1]

            exercise = splith[-1]

            return (name, exercise)


    def columns_exercises(self):

        l = []
        headers = self.get_header_range()
        ce = self.challenger_exercises()

        search_items = []
        for key, values in ce.items():
            search_name = ' '.join(key.split('_')).title()
            for v in values:
                search = search_name + " " + v.title()
                search_items.append(search)



        for i in search_items:
           
            d = {}
            for h in headers:
                if h.value == i:
                    d["column"] = h.col
                    d['name'], d['exercise'] = self.parse_header_value(h.value)
                    l.append(d)
                    

        return l
      


    def get_entire_range(self):
        cols = self.sheet.col_count
        rows = self.sheet.row_count
        ran = self.sheet.range('A1:{0}'.format(gspread.utils.rowcol_to_a1(rows, cols)))
        

    def get_header_range(self):
        fc = "B1"   #don't get the Dates column
        lc = gspread.utils.rowcol_to_a1(1, self.sheet.col_count)
        hr = self.sheet.range("{0}:{1}".format(fc, lc))
        return hr

    def get_today_row(self, timezone, day_offset=0):
        now = pendulum.now(tz=timezone)
        d = now.add(days=day_offset)
        date_str = d.format("M/D/YYYY")
        cell = self.sheet.find(date_str)
        return cell.row


    def get_day_total(self, col, timezone, row=None):
        if not row:
            row = get_today_row(timezone)
        v = self.sheet.cell(row, col).value
        try:
            value = int(v)
        except ValueError:
            value = 0

        return value


    def get_total(self, col, timezone, row=None):
        if not row:
            row = self.get_today_row(timezone)
        start = gspread.utils.rowcol_to_a1(2, col)
        end = gspread.utils.rowcol_to_a1(row, col)
        rang = self.sheet.range("{0}:{1}".format(start, end))

        values = [r.value for r in rang]

        l = []
        for v in values:
            try:
                v = int(v)
            except ValueError:
                v = 0

            l.append(v)

        return sum(l)


    def add_count(self, count, col, timezone, row=None):

        if not row:
            row = self.get_today_row(timezone)

        v = self.get_day_total(timezone)
        new = int(v) + int(count)
        self.sheet.update_cell(row, col, new)
        return new






s = Spreadsheet()


def add(col, value, timezone):
    row = s.get_today_row(timezone)
    new = add_count(count=value, col=col, timezone=timezone, row=row)
    return new





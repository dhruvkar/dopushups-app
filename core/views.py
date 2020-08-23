from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import gspread
from gspread.models import Cell
from twilio.twiml.messaging_response import MessagingResponse

from core.utils import Spreadsheet
from core.models import Exercise, Challenger, Column




class IncomingSMS:

    def __init__(self, request):
        self.message_sid = request.GET.get('MessageSid', '')
        self.from_number = request.GET.get('From', '')
        self.to_number = request.GET.get('To', '')
        self.body = request.GET.get('Body', '').lower()

        self.number_of_exercises = 0

        self.challenger = Challenger.objects.filter(phone=self.from_number).first()

        if self.challenger:
            self.cols = self.challenger.column.all()
            self.allowed_codes = [e.sms_code for e in self.challenger.exercises.all()]

            #DO STUFF
            
        else:
            pass


    def make_help_text(self, challenger):
        pass


    def parse_incoming_sms(self, sms):
        if "help" in sms:
            return self.make_help_text()
        else:
            splitsms = sms.split(" ")

            sc = '[' + "".join(self.allowed_codes) + ']'
            add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
            sub_pat = re.compile(r'($-\d{1,})' + '(' +sc+')')

            for ssms in splitsms:
                pass


            pos_count = add_pat.findall(sms)
            neg_count = sub_pat.findall(sms)

            

            if found:
                for f in found:
                    count = f[0]
                    ex_code = f[1]

                    e = Exercise.objects.filter(sms_code=ex_code).first()

                    col = Column.objects.filter(challenger=self.challenger, exercise=e).first()
                    




    def parse_single_instruction(self, instruction):
        """20k or -10"""
        add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
        sub_pat = re.compile(r'($-\d{1,})' + '(' +sc+')')
        if instruction.startswith("-"):
            sub_pat.match(instruction)
        else:
            add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
        pass

def handle_incoming_sms(body):

    sc = '[' + "".join(SMSCODES) + ']'

    pat_re = re.compile('\d{1,}{0}'.format(sc))
    pat_re.findall(body)


@csrf_exempt
def sms_reply(request):

    sms = IncomingSMS(request)

    response = MessagingResponse()
    msg = response.message(sms.challenger.name)
    return HttpResponse(str(response))



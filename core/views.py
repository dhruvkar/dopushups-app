from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import gspread
from gspread.models import Cell
import re
from twilio.twiml.messaging_response import MessagingResponse


import core
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


    def make_how_text(self):
        template = "Hey {0}, you're doing:\n\n{1}.\n\nFor example, text:\n\n'20{2}'\n\nto add 20 {3} to your count.\n\nText 'how' at anytime to get this message again."

        a = self.challenger.exercises.all()
        help0 = self.challenger.name.replace("_", " ").title()
        help1 = ", ".join([str(e) for e in a])

        try:
            e = a[1]
            help3 = e.name
        except IndexError:
            e = a[0]
            help3 = "seconds of {0}".format(e.name)

        help2 = e.sms_code

        return template.format(help0, help1, help2, help3)


    def handle_incoming_sms(self):
        if "how" in self.body:
            return self.make_how_text()
        else:
            splitsms = self.body.split(" ")

            sc = '[' + "".join(self.allowed_codes) + ']'
            add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
            sub_pat = re.compile(r'($-\d{1,})' + '(' +sc+')')

            for ssms in splitsms:
                if ssms.startswith("-"):
                    found = sub_pat.match(ssms)
                else:
                    found = add_pat.match(ssms)

                try:
                    count = found[0]
                except ValueError:
                    count = 0

                exercise = Exercise.objects.filter(sms_code=found[1]).first()
                col = Column.objects.filter(challenger=self.challenger, exercise=e).first()


                core.utils.add(col.number, count, self.challenger.timezone)

            


    def make_response(self, count):
        pass

    def parse_single_instruction(self, instruction):
        """20k or -10"""
        add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
        sub_pat = re.compile(r'($-\d{1,})' + '(' +sc+')')
        if instruction.startswith("-"):
            sub_pat.match(instruction)
        else:
            add_pat = re.compile(r'(\d{1,})' + '(' +sc+')')
        


def handle_incoming_sms(body):

    sc = '[' + "".join(SMSCODES) + ']'

    pat_re = re.compile('\d{1,}{0}'.format(sc))
    pat_re.findall(body)


@csrf_exempt
def sms_reply(request):

    sms = IncomingSMS(request)

    response = MessagingResponse()
    msg = response.message(sms.handle_incoming_sms())
    return HttpResponse(str(response))



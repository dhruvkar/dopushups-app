from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse



@csrf_exempt
def sms_reply(self):

    response = MessagingResponse()
    msg = response.message("Hello world!")
    #msg.media("https://i.imgur.com/HLHBnl9.jpeg")

    return HttpResponse(str(response))
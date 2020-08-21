from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse



@csrf_exempt
def sms_reply(request):

    message_sid = request.GET.get('MessageSid', '')
    from_number = request.GET.get('From', '')
    to_number = request.GET.get('To', '')
    body = request.GET.get('Body', '')
    
    print (from_number)

    response = MessagingResponse()
    msg = response.message(from_number)
    #msg.media("https://i.imgur.com/HLHBnl9.jpeg")

    return HttpResponse(str(response))



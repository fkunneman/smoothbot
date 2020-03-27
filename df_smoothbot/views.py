from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from library.df_response_lib import *
import json

# make sure this repo is in your $PYTHONPATH
from Chefbot_NFC.core import dialog_manager

dm = dialog_manager.DialogManager()

@method_decorator(csrf_exempt, name='dispatch')
def home(request):
    return HttpResponse('Hello World!')

@csrf_exempt
def webhook(request):
    # build request object
    req = json.loads(request.body)
    query = req.get('queryResult')
    fulfillmentText, suggestions, output_contexts = dm.manage(query)
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
       [fulfillmentText, fulfillmentText, False]
    ])
    aog_sc = aog.suggestion_chips(suggestions)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    ff_context = ff_response.output_contexts(req.get('session'),output_contexts)
    reply = ff_response.main_response(ff_text, ff_messages, ff_context)
    # return generated response
    return JsonResponse(reply, safe=False)
 

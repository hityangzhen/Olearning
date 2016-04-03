# -*- coding: utf-8 -*-
from django.conf import settings
from re import compile
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import traceback

EXEMPT_URLS=[compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings,'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:

    def process_request(self, request):
        path = request.path_info.lstrip('/')

        if 'user' not in request.session or not request.session['user']:    
            if not any(m.match(path) for m in EXEMPT_URLS):
            	# print path
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            if path == 'index/' or path == 'login/':
                return HttpResponseRedirect(settings.MAIN_URLS[request.session['user'].usertype])
    

    def process_exception(self,request, exception):
    	return render_to_response('500.html', {'exception':exception,'stackinfo':traceback.format_exc()},
    		context_instance=RequestContext(request))



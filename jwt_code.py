#### belows are testing urls ####

# URL: /test_protect/
@jwt_required
def ApiProtect(request):
    """ this function is made for testing token login
        usage:
            curl -A"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)" -H "signature: <signature>" -H 			 "payload:payload" http://127.0.0.1:8001/test_protect/
    """
    return HttpResponse(json.dumps({ "code":"ok" }),content_type="application/json")

#### belows are auth code ####
def django_jwt_required(view_func):
    """ Check user's signature
    """
    def _check(request, *args, **kwargs):
        ## in the header, we should get "signature" and "payload"
        signature = request.META.get("HTTP_SIGNATURE","")
        payload = request.META.get("HTTP_PAYLOAD","")
        signature = base64.b64decode(signature)
        if rsa.verify(payload, signature, EB_PUBLIC_KEY):
            try:
                payload = json.loads(payload)
            except:
                return HttpResponse(json.dumps({"code":"err", "err_msg":"wrong payload"}),
                                    mimetype='application/json')
            user_id = payload.get("user_id", "")
            agency_id = payload.get("agency_id","")
            exp_time = payload.get("exp","")
            now = datetime.datetime.utcnow()
            if exp_time and now < exp_time:
                try:
                    request.user = User.objects.get(pk=user_id)
                    request.agency = Agency.objects.get(agency_id)
                except:
                    return HttpResponse(json.dumps({"code":"err", "err_msg":"you passed the wrong id"}),
                                        mimetype='application/json')
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps({"code":"err", "err_msg":"expired time error"}),
                                    mimetype='application/json')
        else:
            return HttpResponse(json.dumps({"code":"err", "err_msg":"failed to varify"}),
                                mimetype='application/json')
    return wraps(view_func)(_check)

def jwt_required(fun):
    """ choose different login required function by user_agents of user_agent
        just for apps or pcs
    """
    def choose_endpoint(request):
        ## match apps
        if checkMobile(request):
            return app_verify_tfa_authcode(fun)(request)
        else:#match pcs
            return django_jwt_required(fun)(request)
    return wraps(fun)(choose_endpoint)

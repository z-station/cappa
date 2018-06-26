def check_custom_response(request):
    return '_addanother' not in request.POST and \
           '_continue' not in request.POST and \
           '_popup' not in request.POST


def verify_method(request,method):
    if(request.method == method):
        return True

    else:
        return False


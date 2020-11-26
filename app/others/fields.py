
def verify_fields_none(request, method):
    try:
        email = request.GET.get('email')
        password = request.GET.get('password')
        username = request.GET.get('username')
        token = request.GET.get('token')
        create = request.GET.get('create')
        update = request.GET.get('update')
        delete = request.GET.get('delete')
        superuser = request.GET.get('superuser')
        if((method == 'create')):
            if (((email != None) and (email != '')) and ((password != None) and (password != '')) and ((username != None) and (username != ''))):
                return True
            else:
                return False

        elif((method == 'update')):
            if (((email != None) and (email != '')) and ((password != None) and (password != '')) and ((username != None) and (username != '')) and ((token != None) and (token != ''))):
                return True
            else:
                return False

        elif(method == 'login'):
            if(((email != None) and (email != '')) and ((password != None) and (password != ''))):
                return True
            else:
                return False
        elif((method == 'logout') or (method == 'delete')):
            if(((token != None) and (token != ''))):
                return True
            else:
                return False
        elif((method == 'active')):
            if(((request.META['QUERY_STRING'] != None) and (request.META['QUERY_STRING'] != ''))):
                return True
            else:
                return False

        elif(method == 'change'):
            if(((email != None) and (email != '')) and ((token != None) and (token != ''))):
                return True
            else:
                return False
    except:
        return False

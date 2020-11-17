
def verify_fields_none(request, method):
    try:
        nameproduct = request.GET.get('nameproduct')
        descripction = request.GET.get('descripction')

        if((method == 'create')):
            if(request.GET.get('discount') != None and request.GET.get('price') != None):
                price = float(request.GET.get('price').replace(',', '.'))
                discount = float(request.GET.get('discount').replace(',', '.'))
                if (((nameproduct != None) and (nameproduct != '')) and ((descripction != None) and (descripction != '')) and (price > 0) and (discount > 0)):
                    return True
                else:
                    return False
            elif(request.GET.get('price') != None):
                price = float(request.GET.get('price').replace(',', '.'))
                if(((nameproduct != None) and (nameproduct != '')) and ((descripction != None) and (descripction != '')) and (price > 0)):
                    return True
                else:
                    return False
            else:
                return False
        elif((method == 'update')):
            if(request.GET.get('discount') != None and request.GET.get('price') != None and request.GET.get('id') != None):
                id = int(request.GET.get('id'))
                price = float(request.GET.get('price').replace(',', '.'))
                discount = float(request.GET.get('discount').replace(',', '.'))
                if (((nameproduct != None) and (nameproduct != '')) and ((descripction != None) and (descripction != '')) and (price > 0) and (discount > 0) and (id > 0)):
                    return True
                else:
                    return False
            elif(request.GET.get('price') != None and request.GET.get('id') != None):
                id = int(request.GET.get('id'))
                price = float(request.GET.get('price').replace(',', '.'))
                if(((nameproduct != None) and (nameproduct != '')) and ((descripction != None) and (descripction != '')) and (price > 0) and (id > 0)):
                    return True
                else:
                    return False
            else:
                return False
    except:
        print(Exception)
        return False

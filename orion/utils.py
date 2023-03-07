from datetime import datetime


def converter_data(data):
    if len(data.split('/')) == 3:
        dia, mes, ano  = data.split('/')
    elif len(data.split('-')) == 3:
        dia, mes, ano  = data.split('-')
    else:
        return data;
        #raise Exception("Data inserida Invalida")
    
    return f"{ano}-{mes}-{dia}"
 
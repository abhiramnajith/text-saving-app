from rest_framework.response import Response
from rest_framework import status

def tryexcept(fun):
    def wrapper(*args,**kwargs):
        try:
            output = fun(*args,**kwargs)
            return output
        except Exception as E:
            return Response({'app_data':'Something went wrong','dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)
    return wrapper
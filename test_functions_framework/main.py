from flask import Response
import uuid

def main(request):

    try:
        print("I was called !", uuid.uuid4())
        return Response(response = 'ok', status = 200)
                
    except Exception as e:
        print("ERROR ", e)
        return Response(response = 'AN ERROR OCCURED', status = 400)

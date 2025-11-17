from django.shortcuts import render

# Create your views here.
""" bucket = dict()

def limitRequests(request):
    data = request.data
    
    if bucket[data.get("userId")]==0:
        return "not allowed"
    bucket[data.get("userId")]-=1
    
    return "allowed"
    
    

def refillBucket():
    
    for key in bucket:
        bucket[key]=4
    
    sleep()
    return """
    
    

from django.shortcuts import render

def chatbot_api(request):
    return render(request, 'chatbot_api.html')

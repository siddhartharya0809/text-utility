# I have created this file - Siddharth

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def removepunc(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    FullCaps = request.POST.get('FullCaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')

    # Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char

        parameters = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed

    if FullCaps == "on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        parameters = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        djtext = analyzed

    if extraspaceremover == "on":
        analyzed = ""
        for index, char in enumerate(djtext):
            if not (djtext[index] == " " and djtext[index + 1] == " "):
                analyzed = analyzed + char

        parameters = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed

    if newlineremover == "on":
        analyzed = ""
        for char in djtext:
            if char != "\n" and char != "\r":
                analyzed = analyzed + char

        parameters = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}

    if removepunc != "on" and newlineremover != "on" and extraspaceremover != "on" and FullCaps != "on":
        return HttpResponse("please select any operation and try again")

    return render(request, 'analyze.html', parameters)


def about(request):
    return render(request, 'about.html')
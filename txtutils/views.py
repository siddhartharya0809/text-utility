# I have created this file - Siddharth
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def removepunc(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values for modification
    removepunc_checked = request.POST.get('removepunc', 'off')
    fullcaps_checked = request.POST.get('FullCaps', 'off')
    newlineremover_checked = request.POST.get('newlineremover', 'off')
    extraspaceremover_checked = request.POST.get('extraspaceremover', 'off')
    titlecase_checked = request.POST.get('titlecase', 'off') # NEW
    
    # Check checkbox values for analysis
    wordcount_checked = request.POST.get('wordcount', 'off')
    charcount_checked = request.POST.get('charcount', 'off')

    # Initialize variables
    analyzed_text = djtext
    purposes = [] # A list to hold the purposes of all modifications
    analysis_results = {} # A dictionary to hold analysis results

    # --- Text Modification Pipeline ---
    if removepunc_checked == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        temp_text = ""
        for char in analyzed_text:
            if char not in punctuations:
                temp_text = temp_text + char
        
        analyzed_text = temp_text
        purposes.append('Removed Punctuations')

    # NEW: Title Case logic
    if titlecase_checked == "on":
        analyzed_text = analyzed_text.title()
        purposes.append('Changed to Title Case')

    if fullcaps_checked == "on":
        # Check if title case was also on. If so, this overrides it.
        if 'Changed to Title Case' in purposes:
            purposes.remove('Changed to Title Case') # Remove previous purpose
        analyzed_text = analyzed_text.upper()
        purposes.append('Changed to Uppercase')

    if extraspaceremover_checked == "on":
        temp_text = analyzed_text
        while "  " in temp_text:
            temp_text = temp_text.replace("  ", " ")
        
        analyzed_text = temp_text.strip() # Also remove leading/trailing spaces
        purposes.append('Removed Extra Spaces')

    if newlineremover_checked == "on":
        temp_text = ""
        for char in analyzed_text:
            if char != "\n" and char != "\r":
                temp_text = temp_text + char
        
        analyzed_text = temp_text
        purposes.append('Removed NewLines')
        
    # --- Text Analysis Pipeline ---
    if wordcount_checked == "on":
        words = [word for word in analyzed_text.split() if word.strip()]
        analysis_results['word_count'] = len(words)

    if charcount_checked == "on":
        analysis_results['char_count'] = len(analyzed_text)


    # Check if *any* operation or analysis was selected
    if not purposes and not analysis_results:
        return HttpResponse("Please select at least one operation or analysis and try again")

    # Format the final purpose string
    if purposes:
        final_purpose = ' and '.join(purposes)
    else:
        final_purpose = 'Text Analyzed' # Default if only analysis was done

    # Prepare final parameters for the template
    parameters = {
        'purpose': final_purpose, 
        'analyzed_text': analyzed_text,
        'analysis': analysis_results
    }

    return render(request, 'analyze.html', parameters)


def about(request):
    return render(request, 'about.html')
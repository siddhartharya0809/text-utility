# I have created this file - Siddharth
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# -----------------------------------------------------------------
# VIEW 1: removepunc (Reverted to Text-Only)
# -----------------------------------------------------------------
def removepunc(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values for modification
    removepunc_checked = request.POST.get('removepunc', 'off')
    fullcaps_checked = request.POST.get('FullCaps', 'off')
    newlineremover_checked = request.POST.get('newlineremover', 'off')
    extraspaceremover_checked = request.POST.get('extraspaceremover', 'off')
    titlecase_checked = request.POST.get('titlecase', 'off')
    
    # Check checkbox values for analysis
    wordcount_checked = request.POST.get('wordcount', 'off')
    charcount_checked = request.POST.get('charcount', 'off')

    # Initialize variables
    analyzed_text = djtext
    purposes = [] 
    analysis_results = {}

    # --- Text Modification Pipeline ---
    if removepunc_checked == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        temp_text = ""
        for char in analyzed_text:
            if char not in punctuations:
                temp_text = temp_text + char
        
        analyzed_text = temp_text
        purposes.append('Removed Punctuations')

    if titlecase_checked == "on":
        analyzed_text = analyzed_text.title()
        purposes.append('Changed to Title Case')

    if fullcaps_checked == "on":
        if 'Changed to Title Case' in purposes:
            purposes.remove('Changed to Title Case')
        analyzed_text = analyzed_text.upper()
        purposes.append('Changed to Uppercase')

    if extraspaceremover_checked == "on":
        temp_text = analyzed_text
        while "  " in temp_text:
            temp_text = temp_text.replace("  ", " ")
        
        analyzed_text = temp_text.strip()
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
        final_purpose = 'Text Analyzed' 

    # Prepare final parameters
    parameters = {
        'purpose': final_purpose, 
        'analyzed_text': analyzed_text,
        'analysis': analysis_results
    }
    
    # Render the results page
    return render(request, 'analyze.html', parameters)


# -----------------------------------------------------------------
# VIEW 2: file_utility (NEW)
# -----------------------------------------------------------------
def file_utility(request):
    # Handle POST request (when form is submitted)
    if request.method == 'POST':
        # --- Check for file upload ---
        if 'file_upload' not in request.FILES:
            return render(request, 'file_utility.html', {'error': 'No file was uploaded.'})
            
        uploaded_file = request.FILES['file_upload']
        
        # Limit file size (e.g., 5MB)
        if uploaded_file.size > 5_242_880:
            return render(request, 'file_utility.html', {'error': 'Error: File is too large (Max 5MB).'})
            
        file_content = uploaded_file.read()
        
        # Try to decode as UTF-8
        try:
            djtext = file_content.decode('utf-8')
        except UnicodeDecodeError:
            return render(request, 'file_utility.html', {'error': 'Error: Could not read file. Please ensure it is a UTF-8 encoded text file.'})

        # --- Check checkbox values for modification ---
        removepunc_checked = request.POST.get('removepunc', 'off')
        fullcaps_checked = request.POST.get('FullCaps', 'off')
        newlineremover_checked = request.POST.get('newlineremover', 'off')
        extraspaceremover_checked = request.POST.get('extraspaceremover', 'off')
        titlecase_checked = request.POST.get('titlecase', 'off')
        
        analyzed_text = djtext
        purposes = []

        # --- Text Modification Pipeline ---
        if removepunc_checked == "on":
            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            temp_text = ""
            for char in analyzed_text:
                if char not in punctuations:
                    temp_text = temp_text + char
            analyzed_text = temp_text
            purposes.append('Removed Punctuations')

        if titlecase_checked == "on":
            analyzed_text = analyzed_text.title()
            purposes.append('Changed to Title Case')

        if fullcaps_checked == "on":
            if 'Changed to Title Case' in purposes:
                purposes.remove('Changed to Title Case')
            analyzed_text = analyzed_text.upper()
            purposes.append('Changed to Uppercase')

        if extraspaceremover_checked == "on":
            temp_text = analyzed_text
            while "  " in temp_text:
                temp_text = temp_text.replace("  ", " ")
            analyzed_text = temp_text.strip()
            purposes.append('Removed Extra Spaces')

        if newlineremover_checked == "on":
            temp_text = ""
            for char in analyzed_text:
                if char != "\n" and char != "\r":
                    temp_text = temp_text + char
            analyzed_text = temp_text
            purpos
            es.append('Removed NewLines')
            
        # Check if *any* operation was selected
        if not purposes:
            # If no operation, just return the original file content
            pass 

        # --- Force Download ---
        response = HttpResponse(analyzed_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="analyzed_text.txt"'
        return response

    # Handle GET request (when user just visits the page)
    return render(request, 'file_utility.html')


# -----------------------------------------------------------------
# VIEW 3: about
# -----------------------------------------------------------------
def about(request):
    return render(request, 'about.html')
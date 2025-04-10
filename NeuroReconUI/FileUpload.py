from django.shortcuts import render
from django.http import JsonResponse
import os


def handle_file_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        dir_path = request.POST.get('filePath', '').strip()
        
        
        # Determine the upload directory (you can dynamically create directories as needed)
        #dir_path = os.path.join("FileUpload",request.POST.get('entity', ''))
        
        # Create the directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(dir_path, uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        
        return JsonResponse({'success': True, 'message': 'File uploaded successfully.'})

    return JsonResponse({'success': False, 'message': 'No file uploaded.'})
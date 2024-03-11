from rest_framework import serializers

def validate_pdf_file(file):
    print(f"Received content type for PDF: {file.content_type}")
    if file.content_type != 'application/pdf':
        raise serializers.ValidationError("Only PDF files are allowed.")
    return file

def validate_video_file(file):
    print(f"Received content type for video: {file.content_type}")
    valid_content_types = ['video/mp4', 'video/avi', 'video/mkv', 'video/quicktime']
    if file.content_type not in valid_content_types:
        raise serializers.ValidationError("Invalid video format.")
    return file
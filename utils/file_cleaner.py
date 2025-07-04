import os
import hashlib
from django.conf import settings

def find_duplicates(directory):
    """Find duplicate files in specified directory"""
    unique_files = {}
    duplicates = []
    
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Skip non-media files and cache
            if any(skip in filepath for skip in ['/cache/', '/temp/']):
                continue
                
            # Calculate file hash
            try:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                if file_hash in unique_files:
                    duplicates.append(filepath)
                else:
                    unique_files[file_hash] = filepath
            except (IOError, OSError):
                continue
    
    return duplicates

def clean_duplicates():
    """Remove duplicate files from media directories"""
    media_root = settings.MEDIA_ROOT
    duplicates = find_duplicates(media_root)
    
    for filepath in duplicates:
        try:
            os.remove(filepath)
            print(f"Removed duplicate: {filepath}")
        except (IOError, OSError) as e:
            print(f"Error removing {filepath}: {str(e)}")
    
    return len(duplicates)

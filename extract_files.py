#!/usr/bin/env python3
import os
import re
from pathlib import Path

def create_dirs():
    folders = ["core", "ui", "modules", "database", "assets", "exports", "logs"]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Folders created")

def extract_files():
    mega_files = ["ArewaSchoolManager_setup.txt", "ArewaSchoolManager_remaining.txt"]
    pattern = r'FILE \d+: (.+?)\n=+\n(.*?)(?=\n\nFILE \d+:|=====|$)'
    
    files_count = 0
    for mega_file in mega_files:
        if not os.path.exists(mega_file):
            print(f"⚠️  {mega_file} not found, skipping...")
            continue
        
        with open(mega_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for match in re.finditer(pattern, content, re.DOTALL):
            filename = match.group(1).strip()
            file_content = match.group(2).strip()
            
            if not file_content or filename == "":
                continue
            
            try:
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print(f"✅ Created: {filename}")
                files_count += 1
            except Exception as e:
                print(f"❌ Error creating {filename}: {e}")
    
    return files_count

if __name__ == "__main__":
    print("=" * 60)
    print("ArewaSchool Manager V4 - File Extractor")
    print("=" * 60)
    
    print("\n1️⃣ Creating directories...")
    create_dirs()
    
    print("\n2️⃣ Extracting files...")
    count = extract_files()
    
    print("\n" + "=" * 60)
    print(f"✅ Total files extracted: {count}")
    print("=" * 60)

#!/usr/bin/env python3
"""
Script to remove "Implementation Checklist" sections from ALL problem analysis files.
"""

import os
import re
import glob

def remove_implementation_checklist(file_path):
    """Remove the Implementation Checklist section from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the start of the Implementation Checklist section
        # Look for the pattern: "---\n\n## 📝 Implementation Checklist"
        pattern = r'---\s*\n\s*## 📝 Implementation Checklist.*$'
        
        # Use DOTALL flag to match across newlines
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Remove everything from the Implementation Checklist section onwards
            new_content = content[:match.start()].rstrip() + '\n'
            
            # Write the modified content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def process_folder(folder_path, folder_name):
    """Process all .md files in a folder (excluding summary.md)."""
    # Find all .md files in the directory (excluding summary.md)
    pattern = os.path.join(folder_path, '*.md')
    files = [f for f in glob.glob(pattern) if not f.endswith('summary.md')]
    
    if not files:
        return 0, 0
    
    print(f"\n📁 Processing {folder_name} ({len(files)} files)")
    print("-" * 50)
    
    processed = 0
    removed = 0
    
    for file_path in files:
        processed += 1
        filename = os.path.basename(file_path)
        if remove_implementation_checklist(file_path):
            removed += 1
            print(f"  ✅ {filename}")
        else:
            print(f"  ⚠️  {filename} (no checklist found)")
    
    return processed, removed

def main():
    """Main function to process all problem analysis files."""
    # Get the directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    problem_solutions_dir = os.path.join(script_dir, 'problem_soulutions')
    
    # Get all subdirectories
    subdirs = [d for d in os.listdir(problem_solutions_dir) 
               if os.path.isdir(os.path.join(problem_solutions_dir, d))]
    
    print("🚀 Removing Implementation Checklist sections from ALL problem analysis files")
    print("=" * 80)
    
    total_processed = 0
    total_removed = 0
    
    for subdir in sorted(subdirs):
        folder_path = os.path.join(problem_solutions_dir, subdir)
        processed, removed = process_folder(folder_path, subdir)
        total_processed += processed
        total_removed += removed
    
    print("\n" + "=" * 80)
    print("🎉 Processing complete!")
    print(f"📊 Total files processed: {total_processed}")
    print(f"🗑️  Implementation Checklists removed: {total_removed}")
    print(f"📝 Files without Implementation Checklist: {total_processed - total_removed}")

if __name__ == "__main__":
    main()
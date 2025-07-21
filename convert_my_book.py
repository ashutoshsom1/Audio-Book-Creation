"""
Simple script to convert the RLbook2020.pdf to audiobook
This script uses the AudiobookConverter class to convert your specific book.
"""

import os
import sys
from pathlib import Path
from audiobook_converter import AudiobookConverter

def convert_rl_book():
    """Convert the RLbook2020.pdf to audiobook"""
    
    # Path to your book
    pdf_path = r"C:\Users\ashutosh.somvanshi\Downloads\RLbook2020.pdf"
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Book file not found at: {pdf_path}")
        print("Please make sure the file exists and the path is correct.")
        return False
    
    print("🎧 Starting audiobook conversion for RLbook2020.pdf")
    print("=" * 60)
    
    try:
        # Create converter with English language
        converter = AudiobookConverter(
            pdf_path=pdf_path,
            output_dir="RLbook_audiobook",  # Create specific folder for this book
            language="en",  # English
            slow=False  # Normal speed
        )
        
        print("📖 Converting PDF to audiobook...")
        print("This may take some time depending on the book size...")
        print()
        
        # Convert the book
        result = converter.convert(
            merge_files=True,      # Merge all parts into one file
            cleanup_parts=True     # Remove individual parts after merging
        )
        
        print()
        print("🎉 SUCCESS! Your audiobook is ready!")
        print(f"📁 Location: {result}")
        print()
        print("You can now listen to your audiobook using any audio player.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        print()
        print("💡 Troubleshooting tips:")
        print("1. Make sure all required packages are installed: pip install -r requirements.txt")
        print("2. Check if you have internet connection (required for gTTS)")
        print("3. Ensure the PDF file is not corrupted and contains readable text")
        
        return False

if __name__ == "__main__":
    print("RLbook2020 to Audiobook Converter")
    print("=" * 40)
    print()
    
    success = convert_rl_book()
    
    if success:
        input("\nPress Enter to exit...")
    else:
        input("\nPress Enter to exit...")
        sys.exit(1)

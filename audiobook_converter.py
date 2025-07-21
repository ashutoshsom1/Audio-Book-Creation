"""
Audiobook Converter - PDF to Audio using Google Text-to-Speech
This script converts PDF books to audiobooks using gTTS (Google Text-to-Speech).
"""

import os
import sys
from pathlib import Path
import logging
from datetime import datetime

# Third-party imports (will be installed)
try:
    from gtts import gTTS
    import PyPDF2
    import argparse
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages using: pip install -r requirements.txt")
    sys.exit(1)

# Optional import for audio merging
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Audio merging will be disabled.")
    print("To enable merging, install: pip install pydub")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('audiobook_converter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AudiobookConverter:
    def __init__(self, pdf_path, output_dir="audiobooks", language="en", slow=False):
        """
        Initialize the AudiobookConverter
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str): Directory to save audio files
            language (str): Language for TTS (default: 'en')
            slow (bool): Speak slowly (default: False)
        """
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.language = language
        self.slow = slow
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"Initialized converter for: {self.pdf_path}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def extract_text_from_pdf(self):
        """
        Extract text from PDF file
        
        Returns:
            str: Extracted text from the PDF
        """
        try:
            logger.info("Starting PDF text extraction...")
            text = ""
            
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                logger.info(f"Processing {total_pages} pages...")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        text += page_text + "\n\n"
                        
                        # Progress indicator
                        if page_num % 10 == 0 or page_num == total_pages:
                            logger.info(f"Processed {page_num}/{total_pages} pages")
                            
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
                        continue
            
            logger.info(f"Text extraction completed. Total characters: {len(text)}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error reading PDF file: {e}")
            raise
    
    def clean_text(self, text):
        """
        Clean and prepare text for TTS
        
        Args:
            text (str): Raw text from PDF
            
        Returns:
            str: Cleaned text
        """
        logger.info("Cleaning text...")
        
        # Remove extra whitespace and normalize line breaks
        text = ' '.join(text.split())
        
        # Replace problematic characters
        text = text.replace('\u2019', "'")  # Right single quotation mark
        text = text.replace('\u2018', "'")  # Left single quotation mark
        text = text.replace('\u201c', '"')  # Left double quotation mark
        text = text.replace('\u201d', '"')  # Right double quotation mark
        text = text.replace('\u2013', '-')  # En dash
        text = text.replace('\u2014', '-')  # Em dash
        
        # Remove page numbers and headers (basic cleanup)
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip very short lines that might be page numbers or headers
            if len(line) > 10:
                cleaned_lines.append(line)
        
        cleaned_text = ' '.join(cleaned_lines)
        logger.info(f"Text cleaned. Final character count: {len(cleaned_text)}")
        
        return cleaned_text
    
    def split_text_into_chunks(self, text, chunk_size=4500):
        """
        Split text into smaller chunks for better TTS processing
        
        Args:
            text (str): Text to split
            chunk_size (int): Maximum characters per chunk
            
        Returns:
            list: List of text chunks
        """
        logger.info(f"Splitting text into chunks of {chunk_size} characters...")
        
        # Split by sentences first
        sentences = text.replace('. ', '.|').split('|')
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size, start new chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        logger.info(f"Text split into {len(chunks)} chunks")
        return chunks
    
    def text_to_speech(self, text_chunks):
        """
        Convert text chunks to speech and save as MP3 files
        
        Args:
            text_chunks (list): List of text chunks to convert
            
        Returns:
            list: List of generated audio file paths
        """
        audio_files = []
        book_name = self.pdf_path.stem
        
        logger.info(f"Starting TTS conversion for {len(text_chunks)} chunks...")
        
        for i, chunk in enumerate(text_chunks, 1):
            try:
                logger.info(f"Processing chunk {i}/{len(text_chunks)}...")
                
                # Create gTTS object
                tts = gTTS(text=chunk, lang=self.language, slow=self.slow)
                
                # Save audio file
                audio_filename = f"{book_name}_part_{i:03d}.mp3"
                audio_path = self.output_dir / audio_filename
                
                tts.save(str(audio_path))
                audio_files.append(audio_path)
                
                logger.info(f"Saved: {audio_filename}")
                
            except Exception as e:
                logger.error(f"Error converting chunk {i} to speech: {e}")
                continue
        
        logger.info(f"TTS conversion completed. Generated {len(audio_files)} audio files.")
        return audio_files
    
    def merge_audio_files(self, audio_files):
        """
        Merge multiple audio files into a single audiobook file
        
        Args:
            audio_files (list): List of audio file paths to merge
            
        Returns:
            str: Path to the merged audio file
        """
        if not PYDUB_AVAILABLE:
            logger.warning("pydub not available. Skipping audio merging.")
            return audio_files
            
        if len(audio_files) <= 1:
            return audio_files[0] if audio_files else None
        
        logger.info("Merging audio files...")
        
        try:
            combined = AudioSegment.empty()
            
            for i, audio_file in enumerate(audio_files, 1):
                logger.info(f"Merging file {i}/{len(audio_files)}: {audio_file.name}")
                audio = AudioSegment.from_mp3(str(audio_file))
                combined += audio
                
                # Add a small pause between chunks
                combined += AudioSegment.silent(duration=1000)  # 1 second pause
            
            # Save merged file
            book_name = self.pdf_path.stem
            merged_filename = f"{book_name}_complete_audiobook.mp3"
            merged_path = self.output_dir / merged_filename
            
            combined.export(str(merged_path), format="mp3")
            logger.info(f"Merged audiobook saved as: {merged_filename}")
            
            return merged_path
            
        except Exception as e:
            logger.error(f"Error merging audio files: {e}")
            return audio_files
    
    def convert(self, merge_files=True, cleanup_parts=True):
        """
        Main conversion method
        
        Args:
            merge_files (bool): Whether to merge all parts into single file
            cleanup_parts (bool): Whether to delete individual part files after merging
            
        Returns:
            str: Path to the final audiobook file
        """
        try:
            logger.info("Starting audiobook conversion process...")
            start_time = datetime.now()
            
            # Step 1: Extract text from PDF
            raw_text = self.extract_text_from_pdf()
            if not raw_text:
                raise ValueError("No text could be extracted from the PDF")
            
            # Step 2: Clean the text
            cleaned_text = self.clean_text(raw_text)
            
            # Step 3: Split into chunks
            text_chunks = self.split_text_into_chunks(cleaned_text)
            
            # Step 4: Convert to speech
            audio_files = self.text_to_speech(text_chunks)
            
            if not audio_files:
                raise ValueError("No audio files were generated")
            
            # Step 5: Merge files if requested and available
            final_file = None
            if merge_files and len(audio_files) > 1 and PYDUB_AVAILABLE:
                final_file = self.merge_audio_files(audio_files)
                
                # Cleanup individual parts if requested and merge was successful
                if cleanup_parts and final_file and isinstance(final_file, Path):
                    logger.info("Cleaning up individual part files...")
                    for audio_file in audio_files:
                        try:
                            audio_file.unlink()
                        except Exception as e:
                            logger.warning(f"Could not delete {audio_file}: {e}")
            else:
                if not PYDUB_AVAILABLE and merge_files:
                    logger.info("Merging disabled due to missing pydub. Individual files will be kept.")
                final_file = audio_files[0] if len(audio_files) == 1 else audio_files
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"Conversion completed successfully!")
            logger.info(f"Total time: {duration}")
            logger.info(f"Final audiobook: {final_file}")
            
            return final_file
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise

def main():
    """Main function to run the audiobook converter"""
    parser = argparse.ArgumentParser(description="Convert PDF books to audiobooks using gTTS")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", default="audiobooks", help="Output directory (default: audiobooks)")
    parser.add_argument("-l", "--language", default="en", help="Language code (default: en)")
    parser.add_argument("-s", "--slow", action="store_true", help="Speak slowly")
    parser.add_argument("--no-merge", action="store_true", help="Don't merge audio files")
    parser.add_argument("--keep-parts", action="store_true", help="Keep individual part files after merging")
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    try:
        # Create converter instance
        converter = AudiobookConverter(
            pdf_path=args.pdf_path,
            output_dir=args.output,
            language=args.language,
            slow=args.slow
        )
        
        # Convert PDF to audiobook
        result = converter.convert(
            merge_files=not args.no_merge,
            cleanup_parts=not args.keep_parts
        )
        
        print(f"\n✅ Audiobook conversion completed successfully!")
        print(f"📁 Output location: {result}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

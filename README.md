# Audiobook Converter

Convert PDF books to audiobooks using Google Text-to-Speech (gTTS).

## Quick Start for Your Book

To convert your RLbook2020.pdf to an audiobook, simply:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the conversion:**
   ```bash
   python convert_my_book.py
   ```

That's it! Your audiobook will be created in the `RLbook_audiobook` folder.

## Features

- ✅ Extract text from PDF files
- ✅ Convert text to natural-sounding speech using Google TTS
- ✅ Split large books into manageable chunks
- ✅ Merge audio files into a single audiobook
- ✅ Progress tracking and detailed logging
- ✅ Multiple language support
- ✅ Clean text processing for better audio quality

## Advanced Usage

### Command Line Interface

You can also use the main script with custom options:

```bash
python audiobook_converter.py "path/to/book.pdf" -o "output_folder" -l "en"
```

### Options:
- `-o, --output`: Output directory (default: audiobooks)
- `-l, --language`: Language code (default: en)
- `-s, --slow`: Speak slowly
- `--no-merge`: Don't merge audio files into single file
- `--keep-parts`: Keep individual part files after merging

### Supported Languages

The converter supports all languages available in Google TTS, including:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh` - Chinese
- And many more...

## Requirements

- Python 3.7 or higher
- Internet connection (required for Google TTS)
- The following Python packages (automatically installed with requirements.txt):
  - gtts (Google Text-to-Speech)
  - PyPDF2 (PDF text extraction)
  - pydub (Audio processing)
  - requests (HTTP requests)

## Output

The converter will create:
- Individual audio files for each text chunk
- A single merged audiobook file (if merge is enabled)
- A log file with conversion details

## Troubleshooting

### Common Issues:

1. **"No audio files were generated"**
   - Check internet connection
   - Verify PDF contains readable text
   - Try with a smaller PDF first

2. **"Error reading PDF file"**
   - Ensure PDF is not password-protected
   - Check file permissions
   - Try with a different PDF

3. **"Missing required package"**
   - Run: `pip install -r requirements.txt`

### Performance Tips:

- Large books (500+ pages) may take 30+ minutes to convert
- The process requires internet connection throughout
- Merged files are typically 1-2MB per page of text

## File Structure

```
audiobook_converter/
├── audiobook_converter.py    # Main converter class
├── convert_my_book.py       # Simple script for your specific book
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .github/
│   └── copilot-instructions.md  # Copilot instructions
└── RLbook_audiobook/       # Output folder (created after conversion)
    ├── RLbook2020_complete_audiobook.mp3  # Final audiobook
    └── audiobook_converter.log            # Conversion log
```

## License

This project is open source and available under the MIT License.

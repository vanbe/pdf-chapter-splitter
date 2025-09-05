# PDF Chapter Splitter

## Project Introduction
`PDF Chapter Splitter` is a Python script designed to automatically split large PDF documents into smaller, manageable chapter files based on the PDF's internal bookmarks (outline) information. The script focuses on extracting **first-level chapters only**, filtering out subsections and other non-chapter content to provide clean chapter splits. This is highly useful for users who need to extract specific chapters from multi-chapter PDFs like textbooks, technical manuals, or academic publications.

## Features
- **First-Level Chapter Detection**: Intelligently identifies and extracts only top-level chapters, filtering out subsections, solutions, and other secondary content.
- **Smart Error Correction**: Uses pattern matching to exclude common non-chapter sections like "Solutions", "Review Questions", "Glossary", etc.
- **Precise Page Range Splitting**: Calculates precise page ranges for each chapter based on bookmark positions and identifies gaps as "Unidentified Pages" sections.
- **Chapter Summary Generation**: Automatically creates a CSV file containing chapter information (number, name, page ranges, total pages).
- **Interactive Confirmation**: Displays detected chapters and asks for user confirmation before splitting.
- **Robust Error Handling**: Handles problematic PDFs with advanced error correction for bookmark extraction issues.
- **Output Management**: Saves each chapter as a separate PDF file in a dedicated output directory.
- **Filename Sanitization**: Automatically cleans illegal characters from bookmark titles to ensure valid filenames.
- **Optional Sequencing**: Optionally adds sequential prefixes like `01_`, `02_` to the split files for easier sorting and management.
- **Flexible Output Directory**: Supports specifying an output directory, or automatically creating a subfolder with "_chapters" suffix.

## Requirements
- Python 3.x
- PyPDF2 library

## Installation
1. Clone or download this repository
2. Install the required dependency:
```bash
pip install PyPDF2
```

**Note**: The script requires PDFs with embedded bookmarks/outline information. PDFs without bookmarks cannot be processed.

## Usage
### Command Line Usage
```bash
python pdf_chapter_splitter.py <input_pdf_path> [-o <output_directory>] [--no-sequence] [--include-all]
```

**Parameter Description:**
*   `<input_pdf_path>`: **Required**. The full path to the PDF file you want to split.
*   `-o <output_directory>`, `--output_dir <output_directory>`: **Optional**. Specifies the base output directory for the split PDF files.
    *   If this parameter is **not specified**, the script will create a new subfolder in the same directory as the `input_pdf_path`. This subfolder will be named after the input PDF file (without its extension) with "_chapters" suffix, and all split chapter PDFs will be saved into this subfolder.
    *   **Example**: If `my_book.pdf` is in `/path/to/documents/`, and `-o` is not specified, the output directory will be `/path/to/documents/my_book_chapters/`.
    *   If `-o` is specified, the script will create a subfolder with "_chapters" suffix inside the specified directory.
*   `--no-sequence`: **Optional**. A boolean flag. If this flag is included, the split files will **not** have sequential prefixes. By default, files will be prefixed with sequence numbers.
*   `--include-all`: **Optional**. A boolean flag to include all bookmarks, not just top-level chapters. **Note**: This feature is not fully implemented in the current version.

**Usage Examples:**

1.  **Split `my_book.pdf` to the default directory (a subfolder named `my_book_chapters` in the same directory as `my_book.pdf`), with sequence numbers:**
    ```bash
    python pdf_chapter_splitter.py my_book.pdf
    ```

2.  **Split `report.pdf` to a specified directory `/path/to/output/`, with sequence numbers:**
    ```bash
    python pdf_chapter_splitter.py report.pdf -o /path/to/output/
    ```
    This will create `/path/to/output/report_chapters/` directory.

3.  **Split `document.pdf` to the default directory, but without sequence numbers:**
    ```bash
    python pdf_chapter_splitter.py document.pdf --no-sequence
    ```

### Importing as a Module
You can also import and use the `split_pdf_by_chapters` function in your own Python scripts:
```python
from pdf_chapter_splitter import split_pdf_by_chapters

# Example: Split a PDF
input_file = "path/to/your/document.pdf"
output_folder = "path/to/save/chapters"  # Optional, will create subfolder if None
split_pdf_by_chapters(input_file, output_folder, add_sequence=True)
```

## Output Files
When the script runs successfully, it generates:

1. **Individual Chapter PDFs**: Each detected first-level chapter is saved as a separate PDF file.
   - Files are named using sanitized chapter titles (illegal characters replaced with underscores)
   - Optional sequential prefixes (e.g., `01_Chapter_1.pdf`, `02_Chapter_2.pdf`)
   - Unidentified page sections are also saved as separate PDFs

2. **Chapter Summary CSV**: A CSV file named `{original_filename}_chapter_summary.csv` containing:
   - Chapter Number
   - Chapter Name  
   - Start Page
   - End Page
   - Total Pages

## Chapter Detection Logic
The script uses intelligent filtering to identify first-level chapters:

### Included Patterns
- `Chapter X` (where X is a number)
- `Appendix X` (where X is a letter)
- Top-level bookmarks (level 0 in PDF outline)

### Excluded Patterns
The script automatically filters out common non-chapter sections:
- Subsection patterns (e.g., `1.1`, `1.2`, `2.3.4`)
- `Glossary`
- `References` 
- `Index`
- `Solutions`
- `Review Questions`
- `Critical Thinking Questions`
- `Self-Check Questions`
- `Key Concepts`

### Error Correction Features
- **Duplicate Detection**: Prevents duplicate chapters from being created
- **Page Range Validation**: Ensures valid page ranges and handles edge cases
- **Gap Identification**: Detects and handles unidentified page sections between chapters
- **Robust Bookmark Parsing**: Handles problematic PDFs with NullObject issues

## Interactive Process
The script provides an interactive experience:

1. **Analysis Phase**: Displays detected chapters with page ranges
2. **Confirmation Prompt**: Shows all sections to be created and asks for user confirmation
3. **Processing Phase**: Creates PDF files and generates summary CSV
4. **Completion Report**: Shows created files and their page ranges

## Troubleshooting

### Common Issues
1. **"No outline/bookmarks found in PDF"**: The PDF doesn't have embedded bookmarks. The script cannot process PDFs without bookmark information.

2. **"No top-level chapters found"**: The PDF's bookmarks don't match the expected chapter patterns. The script will attempt to use all bookmarks as a fallback.

3. **"Warning: Could not get page number for bookmark"**: Some bookmarks may point to invalid locations. The script will skip these and continue processing valid bookmarks.

4. **Unidentified page sections**: Pages that fall between chapters or before the first chapter are saved as "Unidentified Pages" sections.

### Tips for Best Results
- Works best with academic textbooks, technical manuals, and professionally formatted PDFs
- Ensure your PDF has a proper table of contents with bookmarks
- The script is designed for PDFs with clear chapter structure (Chapter 1, Chapter 2, etc.)

## Running Tests
The test directory contains a basic test script. To run it:
```bash
python test/test_pdf_splitter.py
```

**Note**: You'll need to modify the test file to point to an actual PDF file for testing.

## License

This project is licensed under the MIT License.
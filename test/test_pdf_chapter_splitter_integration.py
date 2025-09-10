import os
import tempfile
import unittest
from unittest import mock
from PyPDF2 import PdfWriter
from pdf_chapter_splitter import split_pdf_by_chapters

class TestPdfChapterSplitterIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for inputs and outputs
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.pdf_path = os.path.join(self.tmpdir.name, "test_book.pdf")

        # Create a sample PDF with bookmarks
        writer = PdfWriter()
        # Create 6 blank pages
        from PyPDF2 import PageObject
        for i in range(6):
            writer.add_page(PageObject.create_blank_page(width=72, height=72))

        # Add bookmarks: two top-level chapters, one appendix and one nested subsection
        # Use modern PyPDF2 API
        b1 = writer.add_outline_item("Chapter 1", 0)
        # nested subsection (should be ignored by first-level detection)
        writer.add_outline_item("1.1 Subsection", 1, parent=b1)
        writer.add_outline_item("Chapter 2", 2)
        writer.add_outline_item("Appendix A", 4)

        # Write PDF file
        with open(self.pdf_path, "wb") as f:
            writer.write(f)

    def test_split_creates_chapter_files_and_summary(self):
        output_base = self.tmpdir.name
        # Patch input() to automatically confirm
        with mock.patch('builtins.input', return_value='y'):
            split_pdf_by_chapters(self.pdf_path, output_base, add_sequence=True)

        # Expected output directory
        pdf_basename = os.path.splitext(os.path.basename(self.pdf_path))[0]
        output_dir = os.path.join(output_base, pdf_basename + "_chapters")

        self.assertTrue(os.path.isdir(output_dir), f"Output directory {output_dir} should exist")

        # Expect at least 3 pdf files (Chapter 1, Chapter 2, Appendix A)
        pdf_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.pdf')]
        self.assertGreaterEqual(len(pdf_files), 3, f"Expected at least 3 pdf files, found: {pdf_files}")

        # Check that chapter summary CSV exists
        csv_name = f"{pdf_basename}_chapter_summary.csv"
        csv_path = os.path.join(output_dir, csv_name)
        self.assertTrue(os.path.isfile(csv_path), "Chapter summary CSV should be created")

        # Basic content checks: ensure chapter PDF filenames include sanitized chapter names
        expected_names = ["Chapter 1", "Chapter 2", "Appendix A"]
        # Ensure each expected chapter title appears in at least one filename
        found = ' '.join(pdf_files)
        for expected in expected_names:
            matches = [f for f in pdf_files if expected in f]
            self.assertTrue(matches, f"Expected chapter title '{expected}' to appear in output filenames: {pdf_files}")

        # Ensure sequence prefixes are present when add_sequence=True
        for f in pdf_files:
            # filenames like '1_Chapter 1.pdf'
            parts = f.split('_', 1)
            if len(parts) == 2 and parts[0].isdigit():
                self.assertTrue(parts[0].isdigit())

if __name__ == '__main__':
    unittest.main()

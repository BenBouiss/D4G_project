from pypdf import PdfReader, PdfWriter

def extract_pages(input_pdf_path, output_pdf_path, page_numbers):
    """
    Extracts specific pages from a PDF and saves them to a new file.

    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to save the extracted pages.
    :param page_numbers: List of page numbers to extract (1-based indexing).
    """
    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page_number in page_numbers:
            if 1 <= page_number <= len(reader.pages):
                writer.add_page(reader.pages[page_number - 1])
            else:
                print(f"Page {page_number} is out of range. Skipping.")

        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"Extracted pages saved to {output_pdf_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
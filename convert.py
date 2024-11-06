import os
import fitz  # PyMuPDF

def convert_pdfs_to_text(pdf_dir, output_dir):
    # Check if the input PDF directory exists
    if not os.path.exists(pdf_dir):
        print(f"The directory {pdf_dir} does not exist.")
        return
    
    # Check if the output directory exists
    if not os.path.exists(output_dir):
        print(f"The directory {output_dir} does not exist.")
        return
    
    # Iterate over all files in the PDF directory
    for filename in os.listdir(pdf_dir):
        # Check if the file is a PDF
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            doc = fitz.open(pdf_path)
            
            # Extract text from the PDF
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            # Save the extracted text to a new text file in the output directory
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_path = os.path.join(output_dir, text_filename)
            with open(text_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
                
            print(f"Converted {filename} to {text_filename}")

if __name__ == "__main__":
    # Specify the input and output directories
    pdf_directory = "pdfs"  # Directory where PDFs are located
    output_directory = "input"  # Directory where text files will be saved
    convert_pdfs_to_text(pdf_directory, output_directory)

from pdfminer.high_level import extract_text
import nltk
import json
import os
import glob

class PDFProcessor:
    def __init__(self, pdf_path):
        """Initialize the PDF processor with the path to the PDF file."""
        self.pdf_path = pdf_path
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        # Ensure output directory exists
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_text_from_pdf(self):
        """Extract text content from the PDF file."""
        try:
            text = extract_text(self.pdf_path)
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def chunk_text(self, text, min_chunk_size=200):
        """Split the text into manageable chunks using NLTK."""
        # First split into sentences
        sentences = nltk.sent_tokenize(text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size + sentence_size > min_chunk_size and current_chunk:
                # Join the current chunk and add it to chunks
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def save_chunks(self, chunks):
        """Save the processed chunks to a JSON file in the output directory."""
        try:
            # Get the PDF filename without extension
            pdf_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
            # Create output filename in the output directory
            output_file = os.path.join(self.output_dir, f"processed_{pdf_filename}.json")
            
            data = {
                "source_pdf": self.pdf_path,
                "chunks": chunks,
                "total_chunks": len(chunks)
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return output_file
        except Exception as e:
            print(f"Error saving chunks: {e}")
            return None

def process_pdf(pdf_path):
    """Process a single PDF file."""
    print(f"\nProcessing PDF: {pdf_path}")
    processor = PDFProcessor(pdf_path)
    
    # Check if output file already exists
    output_file = os.path.join(processor.output_dir, f"processed_{os.path.splitext(os.path.basename(pdf_path))[0]}.json")
    if os.path.exists(output_file):
        print(f"Output file already exists: {output_file}")
        return True
    
    # Extract text from PDF
    print("Extracting text...")
    text = processor.extract_text_from_pdf()
    if text is None:
        print("Failed to extract text from PDF")
        return False
    
    # Chunk the text
    print("Chunking text...")
    chunks = processor.chunk_text(text)
    print(f"Created {len(chunks)} text chunks")
    
    # Save chunks to JSON
    output_file = processor.save_chunks(chunks)
    if output_file:
        print(f"Successfully saved chunks to {output_file}")
        return True
    else:
        print("Failed to save chunks")
        return False

def process_all_pdfs(pdf_dir="PDF"):
    """Process all PDFs in the specified directory."""
    # Get list of all PDF files
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir} directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    successful = 0
    failed = 0
    skipped = 0
    
    for pdf_file in pdf_files:
        try:
            result = process_pdf(pdf_file)
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            failed += 1
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Failed to process: {failed}")
    print(f"Skipped (already processed): {skipped}")

def main():
    # Process all PDFs in the PDF directory
    process_all_pdfs()

if __name__ == "__main__":
    main()

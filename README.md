# PDF to Chatbot Processor

A Python tool to process PDF documents into structured JSON format suitable for chatbot training or knowledge base creation.

## Features

- Extract text from PDF files using `pdfminer.six`
- Split text into meaningful chunks using NLTK
- Process multiple PDFs in batch
- Save processed content in JSON format
- Skip already processed files
- Organized output structure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Uththunga/PDF2JSON.git
cd PDF2JSON
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF files in the `PDF` directory
2. Run the processor:
```bash
python pdf_processor.py
```

The script will:
- Process all PDFs in the PDF directory
- Create chunks of text with proper context
- Save processed files in the `output` directory
- Skip already processed files
- Provide a processing summary

## Output Format

The processed files are saved as JSON with the following structure:
```json
{
    "source_pdf": "path/to/pdf",
    "chunks": ["chunk1", "chunk2", ...],
    "total_chunks": number_of_chunks
}
```

## Project Structure

```
PDF2JSON/
├── PDF/                    # Place PDF files here
├── output/                 # Processed JSON files
├── pdf_processor.py        # Main processing script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies

- pdfminer.six: For PDF text extraction
- nltk: For text processing and chunking
- Python 3.6+

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

MIT License - feel free to use this project for your own chatbot or knowledge base creation.

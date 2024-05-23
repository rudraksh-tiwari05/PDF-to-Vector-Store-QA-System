```markdown
# PDF to Vector Store QA System

This project extracts text from a PDF file, indexes it using a vector store in Cassandra, and allows users to ask questions based on the content of the PDF. The system leverages Langchain, OpenAI's LLM, and vector embeddings to provide accurate answers.

## Prerequisites

- Python 3.7+
- Virtual environment (recommended)
- Necessary Python packages (see below)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/pdf-vectorstore-qa.git
   cd pdf-vectorstore-qa
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**

   Create a `.env` file in the project root directory and add the following environment variables:

   ```env
   ASTRA_DB_APP_TOKEN=your_astra_db_app_token
   ASTRA_DB_ID=your_astra_db_id
   OPEN_API_KEY=your_openai_api_key
   PDF_FILE_PATH=path/to/your/file.pdf
   ```

## Usage

1. **Run the Script**

   ```bash
   python main.py
   ```

2. **Interact with the System**

   - The system will prompt you to enter your questions based on the PDF content.
   - Type your questions and receive answers from the vector store.
   - Type `quit` to exit the interaction loop.

## Project Structure

```
pdf-vectorstore-qa/
│
├── .env.example       # Example environment variables file
├── main.py            # Main script to run the QA system
├── requirements.txt   # List of Python dependencies
├── README.md          # Project documentation
└── ...
```

## Key Components

- **Langchain**: Used for text processing and vector store management.
- **OpenAI**: Provides language models for question answering.
- **PyPDF2**: Extracts text from PDF files.
- **Cassandra**: Stores vector embeddings for efficient querying.

## Troubleshooting

- Ensure all environment variables are correctly set.
- Check that the PDF file path is correct.
- Verify internet connectivity for API calls.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Author
```
Rudraksh Tiwari 
```
```
##License
This project is licensed under the MIT License. See the LICENSE file for details.
```
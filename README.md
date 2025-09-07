# AISocialPros Studio

A Streamlit web application that generates marketing articles using OpenAI's GPT API, based on user-provided topics and style examples.

## Features

- **Topic-based Article Generation**: Provide a topic and get AI-generated marketing content
- **Style Matching**: Use up to 3 example articles to match your preferred writing style
- **Multi-tab Interface**: Organized workflow with separate tabs for input, examples, results, and archive
- **Article Archive**: All generated articles are automatically saved and accessible
- **Generation Logging**: Complete log of all generation requests for analysis
- **Download Support**: Download individual articles as text files

## Installation

1. Clone or download this project
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Get an OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys)
2. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Follow the workflow:
   - **Tab 1**: Enter your article topic (API key is automatically loaded from .env)
   - **Tab 2**: Provide up to 3 URLs of example articles for style reference
   - **Tab 3**: Generate and view your new article
   - **Tab 4**: Browse your article archive

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── articles/             # Directory for saved articles (auto-created)
├── generation_log.json   # Log of all generation requests (auto-created)
└── README.md             # This file
```

## Features Details

### Article Generation
- Uses OpenAI's GPT-5 model
- Incorporates style examples from provided URLs
- Generates 500-800 word marketing articles
- Maintains professional and engaging tone

### Archive System
- Automatic file naming with timestamps
- Chronological organization (newest first)
- Individual download options
- Full content preview

### Logging
- Complete generation history
- Topic and example URL tracking
- Timestamp recording
- JSON format for easy analysis

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for URL fetching and API calls

## Notes

- The URL content fetching is simplified and may not work with all websites
- For production use, consider implementing proper HTML parsing and content extraction
- Rate limits apply based on your OpenAI API plan
- Articles are stored locally in the `articles/` directory

## Security

- API keys are handled securely and not stored persistently
- All data remains local to your machine
- No external data transmission except to OpenAI API

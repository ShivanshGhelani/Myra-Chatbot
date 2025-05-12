# MyraChatBot - AI Assistant Powered by Groq API

## Overview

MyraChatBot is a modern, responsive AI assistant web application built with FastAPI that leverages the power of Groq's large language models to provide intelligent conversation, text summarization, and scenario description capabilities. The application features a sleek web interface that makes interacting with AI models intuitive and seamless.

<div align="center">
  <img src="static/SVG/bot.svg" alt="MyraChatBot Logo" width="64" height="64">
</div>

## Screenshots

### Chat Interface
![Chat Interface](screenshots/chat-interface.png)
*The main chat interface where users can interact with the AI assistant*

### Text Summarization
![Text Summarization](screenshots/summarization.png)
*Text summarization feature in action*

### Visual Scene Description
![Scene Description](screenshots/scene-description.png)
*The AI generating descriptions from detected objects*

## Features

- **AI-Powered Chat**: Have natural conversations with advanced AI models (Llama3-70B or Mixtral-8x7B)
- **Text Summarization**: Generate concise summaries of any text input
- **Visual Scenario Description**: Generate natural language descriptions from object detection data
- **User-Friendly Interface**: Modern, responsive UI with code highlighting and markdown support
- **Chat History Persistence**: Save and load past conversations
- **Configurable Settings**: Easily customizable through environment variables

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Provider**: Groq API (supports multiple LLM models)
- **Frontend**: HTML/CSS/JavaScript
- **Containerization**: Virtual environment management
- **Syntax Highlighting**: Prism.js for code blocks

## Project Structure

```
MyraChatBot/
│
├── api/                  # API module
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   └── routes.py         # API router configuration
│
├── audio/                # Directory for audio files
│
├── config/               # Configuration module
│   ├── settings.py       # Application settings
│   └── voice_mapping.py  # Voice configuration
│
├── core/                 # Core functionality
│   └── chat.py           # ChatManager implementation
│
├── logs/                 # Log files
│   └── app.log
│
├── myra-bot/             # Virtual environment
│
├── routes/               # API route implementations
│   └── chat_routes.py    # Chat-related endpoints
│
├── static/               # Static files
│   ├── favicon.ico
│   ├── profile-photo.jpg
│   ├── resume.pdf
│   └── SVG/              # SVG assets
│      ├── bot.svg
│      └── user.svg
│
└── templates/            # HTML templates
    └── bot.html          # Main UI template
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the main chat interface |
| `/chat` | POST | Process chat requests |
| `/summarize` | POST | Generate text summaries |
| `/scenario` | POST | Generate descriptions from object detection data |

## Setup and Installation

### Prerequisites

- Python 3.9+
- [Groq API key](https://console.groq.com)
- Modern web browser

### Environment Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd MyraChatBot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv myra-bot
   myra-bot\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install fastapi uvicorn groq python-dotenv
   ```

4. Create a `.env` file in the root directory:
   ```
   Username=YourUsername
   Assistantname=Myra
   GroqAPIKey=your_groq_api_key_here
   ```

### Running the Application

1. Start the server:
   ```
   uvicorn api.main:create_app --host 0.0.0.0 --port 8000 --reload
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Usage Examples

### Chat Interaction

Send a POST request to `/chat` with:
```json
{
  "query": "What is the capital of France?",
  "userName": "User"
}
```

### Text Summarization

Send a POST request to `/summarize` with:
```json
{
  "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
}
```

### Scenario Description

Send a POST request to `/scenario` with:
```json
{
  "status": "success",
  "filename": "image.jpg",
  "detections": {
    "person": [
      {
        "object_id": "person_1",
        "position": "center",
        "confidence": 0.95
      }
    ],
    "dog": [
      {
        "object_id": "dog_1",
        "position": "bottom-right",
        "confidence": 0.87
      }
    ]
  }
}
```

## Configuration Options

The application can be configured through the `.env` file:

- `Username`: Default username for interactions
- `Assistantname`: Name of the AI assistant
- `GroqAPIKey`: Your Groq API key for accessing LLM models

## Logging

Logs are stored in `logs/app.log` and include:
- API request/response details
- Error information
- System messages

## Error Handling

The application includes comprehensive error handling for:
- API connection issues
- Empty or invalid inputs
- Model availability problems
- Configuration errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

### Adding Screenshots

To add screenshots to the README:

1. Take screenshots of the application showing various features
2. Save the screenshots in the `screenshots` directory with descriptive names
3. Update the image paths in the README if necessary
4. Make sure screenshots are clear and demonstrate the feature effectively

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Groq](https://console.groq.com) - AI provider
- [Prism.js](https://prismjs.com/) - Syntax highlighting

# Myra ChatBot

A FastAPI-based chatbot application.

## Features

- AI-powered chatbot interface
- FastAPI backend
- Easy deployment to Vercel

## Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```
   uvicorn app.main:app --reload
   ```

## Deployment

This project is configured for easy deployment to Vercel.

1. Push to GitHub
2. Connect your GitHub repository to Vercel
3. Deploy

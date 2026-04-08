# imgdetect.py

## Description

`imgdetect.py` is a Python script that uses AI (via OpenRouter and an OpenAI-compatible API) to analyze images from a URL and generate descriptive insights.

The script sends both text and image input to a multimodal AI model, which interprets the image and returns a natural language response describing its contents.

This is useful for tasks like image understanding, caption generation, visual QA, and accessibility features.

## Features

- **Multimodal AI Support**: Sends both text and image input to the model.
- **Image URL Analysis**: Processes images directly from publicly accessible URLs.
- **Dynamic Model Selection**: Uses a model specified via environment variable.
- **Flexible Prompting**: Customize the question or instruction for image analysis.
- **Environment-Based Config**: Secure API key and model configuration via `.env`.
- **Simple Output**: Prints AI-generated response directly to the console.

## Installation

### Prerequisites

- Python 3.7 or higher
- An OpenRouter API key (https://openrouter.ai)

### Dependencies

Install required packages:

```bash
pip install openai python-dotenv

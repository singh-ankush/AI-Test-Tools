# imagegen.py

## Description

`imagegen.py` is a Python script that uses AI (via OpenRouter and the OpenAI-compatible API) to generate images from text prompts. It sends a prompt to an AI image generation model and saves the returned image(s) locally in standard formats like PNG.

The script also automatically opens the generated image on supported systems (e.g., Windows), making it easy to preview results instantly.

## Features

- **AI-Powered Image Generation**: Uses the `"openai/sora-2-pro"` model via OpenRouter to generate images from text prompts.
- **Base64 Image Handling**: Decodes base64 image data returned by the API.
- **Automatic File Saving**: Saves generated images with incremented filenames.
- **Instant Preview**: Automatically opens generated images (Windows support).
- **Environment-Based Config**: Secure API key management using `.env`.
- **Multiple Image Support**: Handles and saves multiple images if returned.

## Installation

### Prerequisites

- Python 3.7 or higher
- An OpenRouter API key (get one from https://openrouter.ai)

### Dependencies

Install required packages:

```bash
pip install openai python-dotenv

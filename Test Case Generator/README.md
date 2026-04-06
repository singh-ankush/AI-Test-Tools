# testcasegen.py

## Description

`testcasegen.py` is a command-line tool that leverages AI (via OpenAI's API through OpenRouter) to generate structured end-to-end test cases from a text-based context file. It reads requirements, user stories, or product descriptions from a `.txt` file, uses an AI model to create detailed test cases, and exports them to an Excel spreadsheet for easy review and management by QA teams.

Each generated test case includes fields like ID, Title, Description, Preconditions, Steps, Expected Result, and Notes, making it suitable for manual or automated testing workflows.

## Features

- **AI-Powered Generation**: Uses the "nvidia/nemotron-3-nano-30b-a3b:free" model via OpenRouter for generating test cases.
- **Flexible Input**: Accepts any `.txt` file containing context (e.g., requirements, acceptance criteria, edge cases).
- **Structured Output**: Exports test cases to Excel with numbered steps and clear formatting.
- **Configurable Count**: Specify the number of test cases to generate (default: 5).
- **Error Handling**: Robust parsing of AI responses and fallback mechanisms for JSON extraction.
- **CLI Interface**: Simple command-line usage with optional arguments.

## Installation

### Prerequisites

- Python 3.7 or higher (tested on Python 3.14.3).
- An OpenRouter API key (sign up at [openrouter.ai](https://openrouter.ai) if you don't have one).

### Dependencies

Install the required Python packages using pip:

```bash
pip install openai python-dotenv openpyxl
```

### Setup

1. Create a `.env` file in the same directory as `testcasegen.py`.
2. Add your OpenRouter API key to the `.env` file:

   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

   Replace `your_api_key_here` with your actual API key.

## Usage

Run the script from the command line with the following syntax:

```bash
python testcasegen.py <context_file> [output_file] [--count <number>]
```

### Arguments

- `context_file` (required): Path to the input `.txt` file containing the test context (e.g., requirements or user stories).
- `output_file` (optional): Path for the output Excel file (default: `testcases.xlsx`).
- `--count` (optional): Number of test cases to generate (default: 5).

### Example

Assuming you have a file named `login_testplan.txt` with login feature details:

```bash
python testcasegen.py login_testplan.txt login_testcases.xlsx --count 10
```

This will:
- Read the context from `login_testplan.txt`.
- Generate 10 test cases using AI.
- Save the results to `login_testcases.xlsx`.

### Sample Input File

Create a `.txt` file (e.g., `login_testplan.txt`) with content like:

```
Feature: User Login
Requirements:
- Users can log in with email and password.
- Password must be at least 8 characters.
Acceptance Criteria:
- Successful login redirects to dashboard.
- Invalid credentials show error message.
Edge Cases:
- Empty fields, SQL injection attempts, session timeout.
```

### Output

The Excel file will have a sheet named "Test Cases" with the following columns:

- **Test Case ID**: A unique identifier (e.g., TC001).
- **Title**: A brief title for the test case.
- **Description**: Detailed description of what the test covers.
- **Preconditions**: Any setup required before running the test.
- **Steps**: Numbered list of actions (e.g., "1. Navigate to login page\n2. Enter email...").
- **Expected Result**: What should happen if the test passes.
- **Notes**: Additional comments or edge case details.

## Troubleshooting

- **ImportError for openpyxl/openai**: Ensure dependencies are installed via `pip install openai python-dotenv openpyxl`.
- **FileNotFoundError**: Verify the input `.txt` file path is correct and the file exists.
- **API Key Issues**: Check your `.env` file and ensure the `OPENROUTER_API_KEY` is set correctly.
- **JSON Parsing Errors**: The script includes fallback cleaning for AI responses; if issues persist, the AI model might have generated malformed JSON—try reducing the `--count` or simplifying the context.
- **No Output**: Confirm your API key has credits/quota on OpenRouter.

## Contributing

Feel free to fork and improve the script. Ensure any changes maintain compatibility with the AI model's expected JSON output format.

## License

This project is open-source. Use at your own risk.

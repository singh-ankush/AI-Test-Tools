import argparse
import json
import os
import re
from openai import OpenAI
import dotenv

try:
    from openpyxl import Workbook
except ImportError:
    raise ImportError(
        "The openpyxl package is required to write Excel files. Install it with: pip install openpyxl"
    )

dotenv.load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def parse_json_array(text: str):
    text = text.strip()
    first_bracket = text.find("[")
    if first_bracket == -1:
        raise ValueError("No JSON array found in model response.")

    depth = 0
    start = None
    for idx, char in enumerate(text[first_bracket:], start=first_bracket):
        if char == "[":
            if start is None:
                start = idx
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : idx + 1])

    raise ValueError("Could not parse balanced JSON array from model response.")


def build_prompt(context: str, count: int) -> str:
    return (
        "You are an expert QA engineer. Using the following context, generate "
        f"{count} full end-to-end test cases. Each test case must be a JSON object with the keys: "
        "id, title, description, preconditions, steps, expected_result, notes. "
        "Steps should be a list of individual step strings. Output only a valid JSON array. "
        "Do not add extra text outside the JSON array.\n\n"
        "Context:\n" + context
    )


def generate_test_cases(context: str, count: int):
    prompt = build_prompt(context, count)

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[
            {"role": "system", "content": "You generate structured QA test cases."},
            {"role": "user", "content": prompt},
        ],
    )

    text = response.choices[0].message.content
    try:
        return parse_json_array(text)
    except ValueError:
        # Attempt to recover a JSON-like payload if there is surrounding text
        cleaned = re.sub(r"^.*?(\[)", "[", text, flags=re.S)
        cleaned = re.sub(r"\](?!.*\])", "]", cleaned, flags=re.S)
        return parse_json_array(cleaned)


def write_excel(test_cases, output_path: str):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Test Cases"

    headers = [
        "Test Case ID",
        "Title",
        "Description",
        "Preconditions",
        "Steps",
        "Expected Result",
        "Notes",
    ]
    sheet.append(headers)

    for case in test_cases:
        steps = case.get("steps") or []
        if isinstance(steps, list):
            steps = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(steps))
        sheet.append(
            [
                case.get("id", ""),
                case.get("title", ""),
                case.get("description", ""),
                case.get("preconditions", ""),
                steps,
                case.get("expected_result", ""),
                case.get("notes", ""),
            ]
        )

    workbook.save(output_path)


def read_context_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Context file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate end-to-end test cases from a text context file and write them to an Excel workbook."
    )
    parser.add_argument(
        "context_file",
        help="Path to the .txt file containing requirements, user stories, or product context.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="testcases.xlsx",
        help="Output Excel file path (default: testcases.xlsx).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of test cases to generate (default: 5).",
    )
    args = parser.parse_args()

    context = read_context_file(args.context_file)
    print(f"Loaded context from {args.context_file}. Generating {args.count} test cases...")

    test_cases = generate_test_cases(context, args.count)
    if not isinstance(test_cases, list):
        raise ValueError("Generated response is not a JSON array of test cases.")

    write_excel(test_cases, args.output_file)
    print(f"Saved {len(test_cases)} test cases to {args.output_file}.")


if __name__ == "__main__":
    main()

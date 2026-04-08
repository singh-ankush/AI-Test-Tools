from openai import OpenAI
import base64
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Generate an image
response = client.chat.completions.create(
  model="openai/sora-2-pro",
  messages=[
          {
            "role": "user",
            "content": "Generate a car crash sunset over the divider in ghibbli style."
          }
        ],
  extra_body={"modalities": ["image"]}
)

# The generated image will be in the assistant message
response = response.choices[0].message
if response.images:
  for i, image in enumerate(response.images):
    image_url = image['image_url']['url']  # Base64 data URL
    if image_url.startswith('data:image/'):
      # Extract format and base64 data
      header, encoded = image_url.split(',', 1)
      img_format = header.split('/')[1].split(';')[0]  # e.g., 'png'
      img_data = base64.b64decode(encoded)
      
      # Save to file
      filename = f"generated_image_{i+1}.{img_format}"
      with open(filename, 'wb') as f:
        f.write(img_data)
      print(f"Image saved as: {filename}")
      
      # Open the image (Windows)
      os.startfile(filename)
    else:
      print(f"Unexpected image URL format: {image_url[:50]}...")

# ✅ Import libraries
import requests
import time
# from IPython.display import Image
from dotenv import load_dotenv
import os
# ✅ Upload your image
# from google.colab import files
# uploaded = files.upload()       

def extract_text_from_image(image_path="public/trial.jpg"):
    """
    Extract text from an image using Azure OCR API.
    Args:
        image_path (str): Path to the image file
    Returns:
        str: Extracted text from the image
    """
    # Load environment variables
    load_dotenv()

    # Debug prints
    print("ENDPOINT:", os.getenv("ENDPOINT"))
    print("AZURE_API_KEY:", os.getenv("AZURE_API_KEY"))

    # ✅ Display the image
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # ✅ Read the image bytes
    with open(image_path, "rb") as f:
        image_data = f.read()

    # ✅ Azure Read API endpoint
    endpoint = os.getenv("ENDPOINT")
    if not endpoint:
        raise ValueError("ENDPOINT environment variable is not set. Please check your .env file.")

    ocr_url = f"{endpoint}/vision/v3.2/read/analyze"

    api_key = os.getenv("AZURE_API_KEY")
    if not api_key:
        raise ValueError("AZURE_API_KEY environment variable is not set. Please check your .env file.")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream"
    }

    # ✅ Step 1: Send image to Azure
    print("Submitting image to Azure OCR API...")
    print("URL:", ocr_url)  # Debug print
    response = requests.post(ocr_url, headers=headers, data=image_data)
    if response.status_code != 202:
        print("❌ Error:", response.status_code)
        print(response.text)
        raise Exception("Azure OCR request failed.")

    # ✅ Step 2: Poll for result
    operation_url = response.headers["Operation-Location"]
    print("Waiting for OCR results...")

    while True:
        result_response = requests.get(operation_url, headers=headers)
        result_json = result_response.json()
        status = result_json["status"]

        if status == "succeeded":
            break
        elif status == "failed":
            raise Exception("OCR failed.")
        time.sleep(1)

    # ✅ Step 3: Extract and return text
    extracted_text = []
    for result in result_json["analyzeResult"]["readResults"]:
        for line in result["lines"]:
            extracted_text.append(line["text"])
    
    return "\n".join(extracted_text)

# Initialize variable to None - will be set when function is called
INGREDIENTS_TEXT = None

if __name__ == "__main__":
    # If this file is run directly, extract text and print it
    INGREDIENTS_TEXT = extract_text_from_image()
    print("\n📝 Extracted Text:")
    print(INGREDIENTS_TEXT)
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(r'C:/Users/path to your file/API.env')  # Load the variables from the file .env

api_key = os.getenv('API_KEY')
cx = os.getenv('CX')

# Use environment variables
print(f'API Key: {api_key}')
print(f'CX: {cx}')

if api_key and cx:
    print("API Key și CX sunt setate corect.")
else:
    print("API Key sau CX lipsește.")


# Reading the list of product codes from the Excel file
def read_product_codes_from_excel(file_path):
    df = pd.read_excel(file_path)
    product_codes = df["ProductCode"].tolist()
    return product_codes

# Function to check if an image contains watermark or inscriptions
def has_watermark_or_inscription(image_url):
    # Implement here the logic of checking the watermark or inscriptions in the image
    # Use image processing services or text recognition

    # Simple example: check if the URL contains "watermark" or "inscription"
    if "watermark" in image_url.lower() or "inscription" in image_url.lower():
        return True
    else: 
        return False
    

def cleanFilename(sourcestring,  removestring =" %:/,\\[]<>*?"):
    """Clean a string by removing selected characters.

    Creates a legal and 'clean' source string from a string by removing some 
    clutter and  characters not allowed in filenames.
    A default set is given but the user can override the default string.

    Args:
        | sourcestring (string): the string to be cleaned.
        | removestring (string): remove all these characters from the string (optional).

    Returns:
        | (string): A cleaned-up string.

    Raises:
        | No exception is raised.
    """
    #remove the undesireable characters
    return ''.join([c for c in sourcestring if c not in removestring])

# Function to save an image in a specified folder
def save_image_to_folder(image_url, output_folder, file_name):
    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # Extract the file name from the URL to use it for local saving
            file_path = os.path.join(output_folder, f"{file_name}.jpg")

            # Save the image in the output file
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Image successfully saved in {file_path}.")
            return file_path
        else:
            print(f"Error downloading the image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading the image: {str(e)}")
        return None

# Function to save the image URLs and to download and save the images in a folder
def search_and_save_images(product_codes, output_folder):
    result_data = {"ProductCode": [], "ImageURL": [], "ImagePath": []}  # Schimbăm structura datelor de rezultat
    for code in product_codes:
        response = requests.get(base_url, params=build_params(code))

        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                result_data["ProductCode"].append(code)
                image_url = data["items"][0].get("link")  # Obținem doar primul URL de imagine
                if image_url and not has_watermark_or_inscription(image_url):
                    image_path = save_image_to_folder(image_url, output_folder, code)
                else:
                    image_url = None
                    image_path = None
                result_data["ImageURL"].append(image_url)
                result_data["ImagePath"].append(image_path)
            else:
                print(f"No results found for product code: {code}")
        else:
            print(f"Error while searching for product code {code} - Status Code: {response.status_code}")

    # Save results in Excel file
    save_image_urls_and_paths_to_excel(result_data, r"C:/Users/path to your file\output_image_URL.xlsx")

# Function to save the image URLs in an Excel file
def save_image_urls_and_paths_to_excel(result_data, excel_file_name):
    df = pd.DataFrame(result_data)
    df.to_excel(excel_file_name, index=False)
    print(f"Image URLs and file path have been saved in {excel_file_name}.")

# Specify the path to the Excel file
excel_file_path = r"C:/Users/path to your file\product_codes.xlsx"

# Call the function to read the list of product codes
product_codes = read_product_codes_from_excel(excel_file_path)
num_results = 3  # Maximum number of desired results for each search
image_size = "large"  # Desired size of the images
image_type = "photo"  # Type of image (can be "photo" or "clipart")

# Base URL for API requests
base_url = "https://www.googleapis.com/customsearch/v1"

# Parameters for the API request
def build_params(query):
    return {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image",
        "num": num_results,
        "imgSize": image_size,
        "imgType": image_type
    }

# Call the function to search and save the image URLs and to download and save the images in a folder.
#output_folder_path = r"E:\Scripturi\Preluare imagini_API_Google\output_images"
output_folder_path = r"C:/Users/path to your file\output_images"

search_and_save_images(product_codes, output_folder_path)
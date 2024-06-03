import requests
from bs4 import BeautifulSoup
import os
import json

def validate_input(subject, num_images):
    if not subject:
        raise ValueError("Subject cannot be empty.")
    if not isinstance(num_images, int) or num_images <= 0:
        raise ValueError("Number of images must be a positive integer.")

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_valid_image_url(url):
    return url and url.startswith('http')

def download_images(subject, num_images):
    validate_input(subject, num_images)
    create_directory('images')
    
    url = 'https://www.bing.com/images/search?q=' + subject
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve web page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('a', class_='iusc')

    image_data = []
    count = 0
    for img_tag in img_tags:
        if count == num_images:
            break
        m = json.loads(img_tag.get('m'))
        image_url = m.get('murl')
        if is_valid_image_url(image_url):
            try:
                print(f"Downloading image {count + 1} from {image_url}")
                img_data = requests.get(image_url).content
                image_filename = f'{count + 1}.jpg'
                image_path = os.path.join('images', image_filename)
                with open(image_path, 'wb') as handler:
                    handler.write(img_data)
                print(f"Saved {image_filename}")
                image_data.append({image_filename: image_url})
                count += 1
            except Exception as e:
                print(f"Failed to download image {image_url}. Error: {e}")
        else:
            print(f"Invalid image URL: {image_url}")
    
    if image_data:
        json_data = {subject: image_data}
        json_filename = os.path.join('images', f'{subject}_image_data.json')
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f'{num_images} images of {subject} downloaded successfully! Image data saved to {json_filename}')
    else:
        print("No valid images found to download.")

try:
    subject = input('Enter the subject for web scraping: ').strip()
    num_images = int(input('Enter the number of images required: ').strip())
    download_images(subject, num_images)
except Exception as e:
    print(f"Error: {e}")

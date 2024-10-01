import requests
from bs4 import BeautifulSoup
import os
import json
import streamlit as st
from PIL import Image
from io import BytesIO
import zipfile
import shutil
# import streamlit.components.v1 as components
def validate_input(subject, num_images):
    if not subject:
        raise ValueError("Subject cannot be empty.")
    if not isinstance(num_images, int) or num_images <= 0:
        raise ValueError("Number of images must be a positive integer.")
#   if num_images > 100:
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
#   return directory
def is_valid_image_url(url):
    return url and url.startswith('http')

def download_images(subject, num_images):
    validate_input(subject, num_images)
    subject_dir = os.path.join('images', subject)
    create_directory(subject_dir)
    
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
        m = img_tag.get('m')
        if m:
            try:
                m = json.loads(m)
                image_url = m.get('murl')
                if is_valid_image_url(image_url):
                    try:
                        img_response = requests.get(image_url, stream=True)
                        if img_response.status_code == 200 and 'image' in img_response.headers['Content-Type']:
                            img = Image.open(BytesIO(img_response.content))
                            if img.mode in ('RGBA', 'P'):
                                img = img.convert('RGBA')
                            else:
                                img = img.convert('RGB')  # Ensure image is in RGB mode for saving as JPEG
                            image_filename = f'{count + 1}.jpg'
                            image_path = os.path.join(subject_dir, image_filename)
                            img.save(image_path, format='JPEG')
                            image_data.append({image_filename: image_url})
                            count += 1
                    except Exception as e:
                        continue  # Skip images that cannot be processed
                else:
                    continue  # Skip invalid image URLs
            except json.JSONDecodeError:
                continue  # Skip tags with invalid JSON
        else:
            continue  # Skip tags without 'm' attribute
    
    if image_data:
        json_data = {subject: image_data}
        json_filename = os.path.join(subject_dir, f'{subject}_image_data.json')
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        st.success(f'{num_images} images of {subject} downloaded successfully! Image data saved to {json_filename}')
        return subject_dir, json_filename
    else:
        st.error("No valid images found to download.")
        return None, None

def zip_directory(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)

st.title('Image Downloader')
st.write('Enter the subject for web scraping and the number of images you want to download.')

subject = st.text_input('Subject')
num_images = st.number_input('Number of images', min_value=1, step=1)

if 'subject_dir' not in st.session_state:
    st.session_state.subject_dir = None
if 'json_path' not in st.session_state:
    st.session_state.json_path = None

if st.button('Download Images'):
    try:
        subject_dir, json_path = download_images(subject, num_images)
        st.session_state.subject_dir = subject_dir
        st.session_state.json_path = json_path
        
        if subject_dir:
            st.write("Downloaded images:")
            
            # Display exactly three sample images
            image_files = [f for f in os.listdir(subject_dir) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
            num_display_images = min(3, len(image_files))
            for i in range(num_display_images):
                image_path = os.path.join(subject_dir, image_files[i])
                st.image(image_path, caption=image_files[i])
    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.json_path:
    with open(st.session_state.json_path, "rb") as json_file:
        st.download_button(
            label="Download JSON data",
            data=json_file,
            file_name=os.path.basename(st.session_state.json_path),
            mime="application/json"
        )

if st.session_state.subject_dir:
    # Zip the images folder
    zip_path = os.path.join('images', f'{subject}_images')
    zip_directory(st.session_state.subject_dir, zip_path)
    
    with open(f'{zip_path}.zip', "rb") as zip_file:
        st.download_button(
            label="Download Images",
            data=zip_file,
            file_name=f"{subject}_images.zip",
            mime="application/zip"
        )

import os
import json
import cv2
import shutil
from transformers import pipeline
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# Function to load JSON data from file
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to perform image analysis using OpenCV
import cv2

import cv2

def analyze_image(image_path):
    try:
        print(f"Attempting to read image at: {image_path}")  # Print the image path
        image = cv2.imread(image_path)
        print(image_path)
        if image is None:
            raise ValueError(f"Failed to read image at {image_path}.")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("1")
        
        # Example: Face detection using Haar cascades
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        print("2")

        if len(faces) > 0:
            return ['face_detected']
        else:
            return []
        
    except Exception as e:
        print(f"Error analyzing image {image_path}: {e}")
        return []




# Function to perform caption analysis using NLTK for keyword extraction
def analyze_caption(caption):
    try:
        # Tokenize caption into words
        words = word_tokenize(caption.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # Calculate frequency distribution
        freq_dist = FreqDist(words)
        
        # Get the most common words (as keywords)
        keywords_extracted = list(freq_dist.keys())[:5]
        
        return keywords_extracted
    except Exception as e:
        print(f"Error analyzing caption: {e}")
        return []

# Function to categorize posts based on image and caption analysis
def categorize_posts(posts):
    categorized_posts = {}
    
    for post in posts:
        image_path = post['filepathofimg']
        caption = post['caption']
        
        # Perform image analysis
        image_keywords = analyze_image(image_path)
        
        # Perform caption analysis
        caption_keywords = analyze_caption(caption)
        
        # Combine keywords from image and caption analysis
        combined_keywords = set(image_keywords + caption_keywords)
        
        # Assign categories based on keywords
        categories = set()
        if 'face_detected' in combined_keywords:
            categories.add('faces')
        if 'travel' in combined_keywords:
            categories.add('travel')
        if 'pets' in combined_keywords:
            categories.add('pets')
        
        # Assign post to categories
        for category in categories:
            if category not in categorized_posts:
                categorized_posts[category] = []
            categorized_posts[category].append(post)
    
    return categorized_posts

# Function to create category folders if they don't exist
def create_category_folders(categories, base_folder):
    for category in categories:
        category_folder = os.path.join(base_folder, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

# Function to save posts into category folders
def save_categorized_posts(categorized_posts, base_folder):
    for category, posts in categorized_posts.items():
        category_folder = os.path.join(base_folder, category)
        for post in posts:
            image_filename = os.path.basename(post['filepathofimg'])
            destination_path = os.path.join(category_folder, image_filename)
            try:
                shutil.copyfile(post['filepathofimg'], destination_path)
                print(f"Saved {image_filename} to {category} folder.")
            except Exception as e:
                print(f"Error saving {image_filename} to {category} folder: {e}")

# Main function
def main():
    
    json_filename = input("Enter JSON filename containing post metadata: ")
    folder_name = input("Enter folder name to save categorized posts: ")

    try:
        # Load JSON data
        posts = load_json(json_filename)

        # Categorize posts based on image and caption analysis
        categorized_posts = categorize_posts(posts)

        # Create category folders
        create_category_folders(categorized_posts.keys(), folder_name)

        # Save categorized posts into category folders
        save_categorized_posts(categorized_posts, folder_name)

        print("Posts have been categorized and saved successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

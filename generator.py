import os
import json
import cv2
import shutil
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import wordnet

# Function to load JSON data from file
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to perform image analysis using OpenCV
def analyze_image(image_path):
    try:
        print(f"Attempting to read image at: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image at {image_path}.")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Example: Face detection using Haar cascades
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

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
        keywords_extracted = list(freq_dist.keys())[:5]  # Extract up to top 5 keywords
        
        # Merge related words into suitable subcategories
        merged_keywords = merge_related_words(keywords_extracted)
        
        return merged_keywords
    
    except Exception as e:
        print(f"Error analyzing caption: {e}")
        return []

# Function to merge related words into suitable subcategories
def merge_related_words(keywords):
    merged_keywords = set()
    
    for keyword in keywords:
        related_words = set()
        
        # Get synonyms for the keyword
        for syn in wordnet.synsets(keyword):
            for lemma in syn.lemmas():
                related_words.add(lemma.name().lower())
        
        # Check if any related word matches with existing merged keywords
        matched = False
        for merged_keyword in merged_keywords:
            if any(word in related_words for word in merged_keyword.split()):
                merged_keyword += f' {keyword}'
                matched = True
                break
        
        if not matched:
            merged_keywords.add(keyword)
    
    return list(merged_keywords)

# Function to categorize posts based on image and caption analysis
def categorize_posts(posts):
    categorized_posts = {}
    
    for post in posts:
        image_path = post['newfilepath']
        caption = post['caption']
        
        # Perform image analysis
        image_keywords = analyze_image(image_path)
        
        # Perform caption analysis
        caption_keywords = analyze_caption(caption)
        
        # Combine keywords from image and caption analysis
        combined_keywords = set(image_keywords + caption_keywords)
        
        # Ensure a post goes to only one subfolder (category)
        assigned_category = None
        for keyword in combined_keywords:
            if keyword in categorized_posts:
                assigned_category = keyword
                break
        
        # If no specific category found, assign to 'general' category
        if not assigned_category:
            assigned_category = 'general'
        
        # Assign post to category
        if assigned_category not in categorized_posts:
            categorized_posts[assigned_category] = []
        categorized_posts[assigned_category].append(post)
    
    return categorized_posts

# Function to create main folder and category subfolders
def create_folders(base_folder, categories):
    try:
        # Create base folder if it doesn't exist
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
        
        # Create subfolders for each category
        for category in categories:
            category_folder = os.path.join(base_folder, category)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
        
        print(f"Created folder structure at: {base_folder}")
    except Exception as e:
        print(f"Error creating folders: {e}")

# Function to save posts into category folders
def save_categorized_posts(categorized_posts, base_folder):
    try:
        # Iterate over each category and save posts
        for category, posts in categorized_posts.items():
            category_folder = os.path.join(base_folder, category)
            for post in posts:
                image_filename = os.path.basename(post['newfilepath'])
                destination_path = os.path.join(category_folder, image_filename)
                try:
                    shutil.copyfile(post['newfilepath'], destination_path)
                    print(f"Saved {image_filename} to {category} folder.")
                except Exception as e:
                    print(f"Error saving {image_filename} to {category} folder: {e}")
    except Exception as e:
        print(f"Error saving categorized posts: {e}")

# Main function
def main():
    json_filename = input("Enter JSON filename containing post metadata: ")
    folder_name = input("Enter folder name to save categorized posts: ")

    try:
        # Load JSON data
        posts = load_json(json_filename)

        # Categorize posts based on image and caption analysis
        categorized_posts = categorize_posts(posts)

        # Get unique categories
        categories = categorized_posts.keys()

        # Create main folder and category subfolders
        create_folders(folder_name, categories)

        # Save categorized posts into category folders
        save_categorized_posts(categorized_posts, folder_name)

        print("Posts have been categorized and saved successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

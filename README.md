# Instagram Post Downloader and Categorizer
This project downloads Instagram posts and categorizes them based on image and caption analysis using three scripts: insta.py, generator.py, and run_all.py.

# Features
Download Instagram Posts: insta.py fetches and downloads images from a specified Instagram profile and saves metadata in JSON format.
Categorize Posts: generator.py analyzes downloaded images and captions to categorize them into different folders.
Sequential Execution: run_all.py manages the sequential execution of both scripts with a single user input.
# Dependencies
Install the necessary Python libraries:
pip install instaloader opencv-python nltk

# Download additional nltk data:

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# Usage
1. Clone the Repository

git clone https://github.com/sagarrh/inscrap.git
cd inscrap

2. Run the Wrapper Script

python runner.py

3. Follow the Prompts
Enter the following information when prompted:

Instagram username
Filename for metadata (e.g., user_posts.json)
Folder name for posts (e.g., downloaded_posts)
Folder name for categorized posts (e.g., categorized_posts)
# Notes
Works only for public accouts
Ensure you have permissions to download content from Instagram.
Categorization is basic and might need enhancements for better accuracy

Instagram Post Downloader and Categorizer
This project contains two scripts, insta.py and generator.py, which respectively download Instagram posts and categorize them based on image and caption analysis. Additionally, a wrapper script run_all.py is provided to manage the sequential execution of these scripts with user input taken once.

Features
Download Instagram Posts: insta.py fetches and downloads images from a specified Instagram profile and saves metadata in JSON format.
Categorize Posts: generator.py analyzes downloaded images and captions to categorize them into different folders.
Sequential Execution: run_all.py manages the sequential execution of both scripts, taking user input once and ensuring generator.py runs only after insta.py completes successfully.
Dependencies
To run these scripts, you need the following Python libraries:

instaloader
opencv-python
nltk
You can install these dependencies using pip:

bash
Copy code
pip install instaloader opencv-python nltk
Additionally, for nltk, you will need to download some data files:

python
Copy code
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
Usage
1. Clone the Repository
bash
Copy code
git clone <repository-url>
cd <repository-folder>
2. Run the Wrapper Script
Execute the wrapper script to run the entire workflow:

bash
Copy code
python run_all.py
3. Follow the Prompts
The script will prompt you to enter the following information:

Instagram username: The Instagram profile from which you want to download posts.
Filename for metadata: The JSON file where the post metadata will be saved.
Folder name for posts: The folder where the downloaded posts will be saved.
Folder name for categorized posts: The folder where the categorized posts will be saved.
Example Input
text
Copy code
Enter Instagram username: example_user
Enter filename to save post metadata (e.g., 'user_posts.json'): user_posts.json
Enter folder name to save posts (will be created if not exist): downloaded_posts
Enter folder name to save categorized posts: categorized_posts
Script Details
insta.py
Description: Downloads images from the specified Instagram profile and saves metadata in JSON format.
Usage: This script is designed to be called by run_all.py and not directly by the user.
Command Line Arguments: <username> <json_filename> <folder_name>
generator.py
Description: Categorizes downloaded posts based on image and caption analysis.
Usage: This script is designed to be called by run_all.py and not directly by the user.
Command Line Arguments: <json_filename> <folder_name>
run_all.py
Description: Wrapper script to run insta.py and generator.py sequentially with user input taken once.
Usage: Run this script directly to execute the entire workflow.
Notes
Ensure you have appropriate permissions to download content from Instagram and use it according to their terms of service.
The categorization is basic and might require further enhancements for more accurate results.
import os
import instaloader
import json
import sys
from datetime import datetime

# Initialize Instaloader
L = instaloader.Instaloader()

# Function to fetch user's media posts
def fetch_user_posts(username):
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()
    return [post for post in posts if post.typename == 'GraphImage']  # Filter out only image posts

# Function to download image posts and save metadata in JSON format
def download_instagram_posts(username, json_filename, folder_name):
    try:
        posts = fetch_user_posts(username)
        post_data = []

        for post in posts:
            # Download the post image
            image_filename = f"{post.mediaid}.jpg"
            image_filepath = os.path.abspath(os.path.join(folder_name, image_filename))

            # Check if image file already exists
            if os.path.exists(image_filepath):
                print(f"Skipping post {post.mediaid} as image file already exists.")
                continue

            try:
                L.download_post(post, target=folder_name)
                print(f"Downloaded post {post.mediaid} as {image_filename}")

                # Prepare post metadata
                base_folder_path = os.path.dirname(image_filepath)
                new_file_path = os.path.join(base_folder_path, f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.jpg")
                
                post_metadata = {
                    'likes': post.likes,
                    'comments': post.comments,
                    'postdate': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
                    'caption': post.caption,
                    'filepathofimg': image_filepath,
                    'newfilepath': new_file_path  # New attribute
                }

                # Append post metadata to list
                post_data.append(post_metadata)

            except Exception as e:
                print(f"Error downloading post {post.mediaid}: {e}")

        # Save post data to JSON file with absolute file paths
        json_path = os.path.abspath(json_filename)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(post_data, json_file, ensure_ascii=False, indent=4)
        print(f"Saved metadata of {len(post_data)} posts to {json_path}")

    except Exception as e:
        print(f"Error fetching or processing posts: {e}")

# Main function
def main():
    if len(sys.argv) != 4:
        print("Usage: python insta.py <username> <json_filename> <folder_name>")
        return

    username = sys.argv[1]
    json_filename = sys.argv[2]
    folder_name = sys.argv[3]

    try:
        download_instagram_posts(username, json_filename, folder_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

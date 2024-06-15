import subprocess

def main():
    # Gather all inputs once
    username = input("Enter Instagram username: ")
    json_filename = input("Enter filename to save post metadata (e.g., 'user_posts.json'): ")
    folder_name = input("Enter folder name to save posts (will be created if not exist): ")
    categorized_folder_name = input("Enter folder name to save categorized posts: ")

    # Run insta.py
    insta_process = subprocess.run(["python", "insta.py", username, json_filename, folder_name])
    
    # Check if insta.py ran successfully
    if insta_process.returncode == 0:
        # Run generator.py
        generator_process = subprocess.run(["python", "generator.py", json_filename, categorized_folder_name])
        if generator_process.returncode != 0:
            print("Error: generator.py did not complete successfully.")
    else:
        print("Error: insta.py did not complete successfully.")

if __name__ == "__main__":
    main()

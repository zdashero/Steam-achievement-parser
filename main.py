import os
import sys
import requests
import json
import threading
from queue import Queue

# Function to get achievement data from the Steam API
def get_achievement_data(appid):
    # CHANGE THIS KEY TO YOUR WEBAPI KEY
    apikey="CHANGE ME"
    # API URL for retrieving achievement data
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={apikey}&appid={appid}"
    # Send GET request to the API
    response = requests.get(url)
    # Parse response as JSON
    data = response.json()
    # Extract achievement data from the response
    return data['game']['availableGameStats'].get('achievements', [])

# Function to download an image from a URL and save it to a folder
def download_image(url, folder):
    # Extract filename from the URL
    filename = url.split('/')[-1]
    # Construct full filepath
    filepath = os.path.join(folder, filename)
    # Open file in binary write mode
    with open(filepath, 'wb') as f:
        # Send GET request to download the image
        response = requests.get(url, stream=True)
        # Get total length of the response (if available)
        total_length = response.headers.get('content-length')
        # If total length is not available, write content directly
        if total_length is None: 
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            # Iterate over response content in chunks and write to file
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                # Print download progress
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

# Worker function to download images in separate threads
def download_worker(queue, images_folder):
    while True:
        item = queue.get()
        if item is None:
            break
        url = item[0]
        # Extract filename from the URL
        filename = url.split('/')[-1]
        # Construct full filepath
        filepath = os.path.join(images_folder, filename)
        # Download image and save to folder
        download_image(url, images_folder)
        queue.task_done()

# Main function to orchestrate the download and processing of achievement data
def main(appid):
    # Retrieve achievement data from the Steam API
    achievement_data = get_achievement_data(appid)
    # Initialize list to store processed achievement data
    output_data = []
    # Folder to store downloaded images
    images_folder = "images"
    # Ensure images folder exists, create if not
    os.makedirs(images_folder, exist_ok=True)
    print("Downloading images...")
    # Initialize queue for downloading images
    image_queue = Queue()
    # Number of worker threads for downloading images
    num_threads = 5
    threads = []
    # Create and start worker threads
    for _ in range(num_threads):
        t = threading.Thread(target=download_worker, args=(image_queue, images_folder))
        t.start()
        threads.append(t)
    # Add image download tasks to the queue
    for achievement in achievement_data:
        icon_url = achievement['icon']
        icongray_url = achievement['icongray']
        image_queue.put((icon_url, images_folder))
        image_queue.put((icongray_url, images_folder))
    # Wait for all tasks in the queue to be processed
    image_queue.join()
    # Add None to the queue for each thread to signal completion
    for _ in range(num_threads):
        image_queue.put(None)
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("\nProcessing achievement data...")
    # Process achievement data and save to output list
    for achievement in achievement_data:
        icon_url = achievement['icon']
        icongray_url = achievement['icongray']
        if 'description' in achievement:
            description = achievement['description']
        else:
            description = ""
        achievement_info = {
            "description": description,
            "displayName": achievement['displayName'],
            "hidden": achievement.get('hidden', 0),
            "icon": f"{images_folder}/{icon_url.split('/')[-1]}",
            "icongray": f"{images_folder}/{icongray_url.split('/')[-1]}",
            "name": achievement['name']
        }
        output_data.append(achievement_info)
    # Save processed achievement data to JSON file
    with open('achievements.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print("Processing complete. Output saved to achievements.json.")

# Entry point of the script
if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <appid>")
        sys.exit(1)
    # Get the appid from command line argument
    appid = sys.argv[1]
    # Call the main function with the provided appid
    main(appid)
import urllib.request
import json
import os
from unidecode import unidecode

# CHANGE THESE SETTINGS!
saveDirectory = './uncensored/'
boardLetter = 's'

print("The current working directory is " + saveDirectory)

# Create a folder for the board
path = os.path.join(saveDirectory, boardLetter)
print("Attempting to create directory for board at %s" % path)
try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed - possible directory already exists" % path)
else:
    print("Successfully created the directory %s" % path)

# Get the 4chan board catalog JSON file and open it
url = f"https://a.4cdn.org/{boardLetter}/catalog.json"
response = urllib.request.urlopen(url)
threadCatalog = json.loads(response.read())

print("BEGINNING 4CHAN IMAGE SCRAPE")
print(f"Current board: {boardLetter}")

downloadCounter = 0

# Loop through all pages of the board
for page in threadCatalog:
    print(f"Processing page {page['page']}...")
    # Loop through all threads on the current page
    for thread in page['threads']:
        thread_id = thread['no']
        semantic_url = thread.get('semantic_url', 'no_title')
        thread_path = os.path.join(saveDirectory, boardLetter, f"{thread_id} - {semantic_url}")

        # Create a directory for the thread
        print(f"Attempting to create directory for thread {thread_path}")
        try:
            os.mkdir(thread_path)
        except OSError:
            print(f"Directory {thread_path} already exists, skipping creation.")
        
        # Get the individual thread JSON file
        thread_url = f"https://a.4cdn.org/{boardLetter}/thread/{thread_id}.json"
        try:
            response = urllib.request.urlopen(thread_url)
            individualThread = json.loads(response.read())
        except Exception as e:
            print(f"Error fetching thread {thread_id}: {e}")
            continue
        
        # Process posts in the thread
        for post in individualThread['posts']:
            # Check if an image was posted
            if 'tim' in post:
                OGfilename = unidecode(post.get('filename', 'Unnamed'))
                renamedFile = str(post['tim'])
                fileExtension = str(post['ext'])
                filename = OGfilename + fileExtension
                try:
                    file_url = f"https://i.4cdn.org/{boardLetter}/{renamedFile}{fileExtension}"
                    urllib.request.urlretrieve(file_url, os.path.join(thread_path, filename))
                    downloadCounter += 1
                    print(f"Downloaded image: {filename}")
                except Exception as e:
                    print(f"File Download Error for {filename}: {e}")

print(f"Image Scrape Completed - {downloadCounter} images downloaded")

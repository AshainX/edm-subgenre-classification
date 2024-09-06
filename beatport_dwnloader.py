import os
import requests
from bs4 import BeautifulSoup
import youtube_dl
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' file not found.")
                print("Please follow these steps:")
                print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
                print("2. Create a project and enable the Google Drive API")
                print("3. Create OAuth 2.0 credentials (Desktop app)")
                print("4. Download the credentials and save as 'credentials.json' in this directory")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, file_path, folder_id):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File uploaded to Google Drive. File ID: {file.get("id")}')

def download_song(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return True
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return False

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def main():
    drive_service = get_drive_service()
    if drive_service is None:
        print("Failed to authenticate with Google Drive. Exiting.")
        return

    folder_name = "Beatport Top 100"
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    print(f"Created folder '{folder_name}' in Google Drive. Folder ID: {folder_id}")

    URL_GENRES = "https://www.beatport.com/genre"

    try:
        print(f"Fetching Beatport genres page...")
        soup_genres = get_soup(URL_GENRES)
        print(f"Beatport genres page fetched successfully.")
    except requests.RequestException as e:
        print(f"Error fetching Beatport genres page: {str(e)}")
        return

    genres = {}
    genre_links = soup_genres.find_all("a", class_="genre")
    if not genre_links:
        print("No genres found. Check the website structure.")
        return

    for tag in genre_links:
        genre_name = tag.text.strip().replace("/", "-")
        genre_href = tag.get('href')
        genres[genre_name] = genre_href
        print(f"Found genre: {genre_name} with href: {genre_href}")

    for genre, href in genres.items():
        genre_folder = genre.replace("/", "-")
        if not os.path.exists(genre_folder):
            os.makedirs(genre_folder)
        
        os.chdir(genre_folder)

        print(f"Processing genre: {genre}")
        
        url_top_100 = f"https://www.beatport.com{href}/tracks"
        try:
            print(f"Fetching Top 100 for {genre}...")
            soup_top_100 = get_soup(url_top_100)
            print(f"Top 100 for {genre} fetched successfully.")
        except requests.RequestException as e:
            print(f"Error fetching top 100 for {genre}: {str(e)}")
            os.chdir("..")
            continue
        
        songs_downloaded = 0
        song_items = soup_top_100.find_all("li", class_="bucket-item")
        if not song_items:
            print(f"No songs found for {genre}.")
            os.chdir("..")
            continue

        for i, li_tag in enumerate(song_items, 1):
            if i > 5:  # Limit to 5 songs per genre for testing
                break
            
            p_tag = li_tag.find("p", class_="buk-track-title")
            if not p_tag:
                print(f"Skipping item without track title.")
                continue
            
            a_tag = p_tag.find("a")
            if not a_tag:
                print(f"Skipping item without track link.")
                continue
            
            song_url = f"https://www.beatport.com{a_tag['href']}"
            song_title = a_tag.text.strip()
            
            print(f"Downloading: {song_title}")
            output_path = f"{genre} - {song_title}.%(ext)s"
            if download_song(song_url, output_path):
                mp3_path = output_path.replace("%(ext)s", "mp3")
                if os.path.exists(mp3_path):
                    try:
                        upload_to_drive(drive_service, mp3_path, folder_id)
                        os.remove(mp3_path)  # Remove local file after upload
                        print(f"Uploaded and removed local file: {mp3_path}")
                    except Exception as e:
                        print(f"Error uploading {mp3_path} to Google Drive: {str(e)}")
                else:
                    print(f"Error: MP3 file not found after download: {mp3_path}")
            else:
                print(f"Failed to download: {song_title}")
            
            songs_downloaded += 1
        
        print(f"Completed processing for genre: {genre}. Total songs downloaded: {songs_downloaded}")
        os.chdir("..")

if __name__ == "__main__":
    main()

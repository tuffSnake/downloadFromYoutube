# Import necessary libraries
import os
import yt_dlp

# --- Configuration ---
# The default directory where the MP4 files will be saved.
# You can change this to any path on your system.
DOWNLOAD_DIR = (
    "downloaded_playlist_videos"  # Changed directory name for playlist videos
)

# --- Prerequisites ---
# Make sure you have the following installed:
# 1. Python 3.8 or higher
# 2. pip (Python package installer)
# 3. ffmpeg (for merging video/audio streams, install via your system's package manager, e.g., `sudo apt install ffmpeg` on Ubuntu,
#    `brew install ffmpeg` on macOS, or download from https://ffmpeg.org/download.html on Windows)
#
# Install Python library:
# pip install yt-dlp


def download_youtube_playlist_as_mp4(
    playlist_url: str, output_path: str = DOWNLOAD_DIR
):
    """
    Downloads all videos from a YouTube playlist as MP4 video files.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        output_path (str): The directory where the MP4 files will be saved.
                           Defaults to 'downloaded_playlist_videos'.

    Returns:
        str: A message indicating success or failure.
    """
    # Create the download directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    # Define yt-dlp options for video download (MP4)
    ydl_opts = {
        # Select the best video and audio streams, preferring MP4 if available.
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        # Output file name template: includes playlist title and video title
        "outtmpl": os.path.join(
            output_path, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        ),
        # 'noplaylist': True, # Removed this option to allow playlist downloading
        "verbose": False,  # Set to True for more detailed output from yt-dlp
        "quiet": False,  # Show output (progress) from yt-dlp, but not overly verbose
        "noprogress": False,  # Show progress bar
        "external_downloader_args": ["-loglevel", "error"],  # Suppress ffmpeg logging
        "merge_output_format": "mp4",  # Ensure the final merged file is MP4
        "ignoreerrors": True,  # Continue downloading even if some videos fail
        "download_archive": os.path.join(
            output_path, "downloaded_videos.txt"
        ),  # Keep track of downloaded videos
    }

    print(
        f"Attempting to download videos from playlist: '{playlist_url}' to '{output_path}'..."
    )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
            return f"Success: All available videos from playlist '{playlist_url}' have been processed. Check '{output_path}'."
    except yt_dlp.utils.DownloadError as e:
        return f"Error downloading playlist: {e}. Please check the playlist URL and ensure ffmpeg is installed and accessible in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- Main execution ---
if __name__ == "__main__":
    # Example YouTube playlist link
    # IMPORTANT: Replace this with the actual YouTube playlist URL you want to download.
    # A public playlist example:
    playlist_link = "https://www.youtube.com/watch?v=BHT_aO-vyPo&list=PLzIgqH81y6PwLIg4d-y9jQWkTW09Dq3QW"  # Replace with your playlist URL

    # You can also ask the user for input
    # playlist_link = input("Enter the YouTube playlist URL: ")

    if playlist_link:
        result_message = download_youtube_playlist_as_mp4(playlist_link, DOWNLOAD_DIR)
        print(result_message)
    else:
        print("No YouTube playlist URL provided. Please enter a valid link.")

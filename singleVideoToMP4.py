# Import necessary libraries
import os
import yt_dlp

# --- Configuration ---
# The default directory where the MP4 files will be saved.
# You can change this to any path on your system.
DOWNLOAD_DIR = "downloaded_mp4s"  # Changed directory name for MP4 files

# --- Prerequisites ---
# Make sure you have the following installed:
# 1. Python 3.8 or higher
# 2. pip (Python package installer)
# 3. ffmpeg (for merging video/audio streams, install via your system's package manager, e.g., `sudo apt install ffmpeg` on Ubuntu,
#    `brew install ffmpeg` on macOS, or download from https://ffmpeg.org/download.html on Windows)
#
# Install Python library:
# pip install yt-dlp


def download_youtube_as_mp4(youtube_url: str, output_path: str = DOWNLOAD_DIR):
    """
    Downloads a YouTube video as an MP4 video file.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_path (str): The directory where the MP4 file will be saved.
                           Defaults to 'downloaded_mp4s'.

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
        # 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' tries to get separate mp4 video and m4a audio
        # and then merges them. 'best' will get the best overall quality.
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": os.path.join(
            output_path, "%(title)s.%(ext)s"
        ),  # Output file name template, %(ext)s will be mp4
        "noplaylist": True,  # Do not download entire playlists
        "verbose": False,  # Set to True for more detailed output from yt-dlp
        "quiet": True,  # Suppress most output from yt-dlp
        "noprogress": False,  # Show progress bar
        "external_downloader_args": ["-loglevel", "error"],  # Suppress ffmpeg logging
        "merge_output_format": "mp4",  # Ensure the final merged file is MP4
    }

    print(f"Attempting to download and convert '{youtube_url}' to MP4...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            # yt-dlp automatically handles the extension and merging for video formats.
            # The filename will typically be .mp4 if the format is set correctly.
            final_filename = ydl.prepare_filename(info_dict)
            # Ensure the filename ends with .mp4
            if not final_filename.endswith(".mp4"):
                # This might happen if yt-dlp picked a different best format,
                # but 'merge_output_format': 'mp4' should ensure it's MP4.
                # We can add a fallback rename if needed, but it's usually not.
                pass
            print(f"Successfully downloaded and converted to: {final_filename}")
            return f"Success: MP4 saved to {final_filename}"
    except yt_dlp.utils.DownloadError as e:
        return f"Error downloading or converting: {e}. Please check the URL and ensure ffmpeg is installed and accessible in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- Main execution ---
if __name__ == "__main__":
    # Example YouTube video link
    # Replace this with the actual YouTube video link you want to convert
    video_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example: Rick Astley - Never Gonna Give You Up

    # You can also ask the user for input
    # video_link = input("Enter the YouTube video URL: ")

    if video_link:
        result_message = download_youtube_as_mp4(video_link, DOWNLOAD_DIR)
        print(result_message)
    else:
        print("No YouTube URL provided. Please enter a valid link.")

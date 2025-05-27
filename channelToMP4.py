# Import necessary libraries
import os
import yt_dlp

# --- Configuration ---
# The default directory where the MP4 files will be saved.
# You can change this to any path on your system.
DOWNLOAD_DIR = "downloaded_channel_videos"  # Changed directory name for channel videos

# --- Prerequisites ---
# Make sure you have the following installed:
# 1. Python 3.8 or higher
# 2. pip (Python package installer)
# 3. ffmpeg (for merging video/audio streams, install via your system's package manager, e.g., `sudo apt install ffmpeg` on Ubuntu,
#    `brew install ffmpeg` on macOS, or download from https://ffmpeg.org/download.html on Windows)
#
# Install Python library:
# pip install yt-dlp


def download_youtube_channel_as_mp4(channel_url: str, output_path: str = DOWNLOAD_DIR):
    """
    Downloads all videos from a YouTube channel as MP4 video files.

    Args:
        channel_url (str): The URL of the YouTube channel (e.g., a channel page, or uploads playlist URL).
        output_path (str): The directory where the MP4 files will be saved.
                           Defaults to 'downloaded_channel_videos'.

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
        # Output file name template: includes channel name and video title
        # %(channel)s will create a subfolder named after the channel.
        # %(upload_date)s can be useful for chronological sorting.
        "outtmpl": os.path.join(
            output_path, "%(channel)s/%(upload_date)s - %(title)s.%(ext)s"
        ),
        "verbose": False,  # Set to True for more detailed output from yt-dlp
        "quiet": False,  # Show output (progress) from yt-dlp, but not overly verbose
        "noprogress": False,  # Show progress bar
        "external_downloader_args": ["-loglevel", "error"],  # Suppress ffmpeg logging
        "merge_output_format": "mp4",  # Ensure the final merged file is MP4
        "ignoreerrors": True,  # Continue downloading even if some videos fail
        "download_archive": os.path.join(
            output_path, "downloaded_channel_videos.txt"
        ),  # Keep track of downloaded videos
    }

    print(
        f"Attempting to download videos from channel: '{channel_url}' to '{output_path}'..."
    )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # yt-dlp can directly handle channel URLs, treating them as a collection of videos.
            ydl.download([channel_url])
            return f"Success: All available videos from channel '{channel_url}' have been processed. Check '{output_path}'."
    except yt_dlp.utils.DownloadError as e:
        return f"Error downloading channel videos: {e}. Please check the channel URL and ensure ffmpeg is installed and accessible in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- Main execution ---
if __name__ == "__main__":
    # Example YouTube channel link
    # IMPORTANT: Replace this with the actual YouTube channel URL you want to download.
    # You can use the main channel URL (e.g., https://www.youtube.com/@YouTube),
    # or the uploads playlist URL (e.g., https://www.youtube.com/playlist?list=UU-x_V_w_gA2X_j_N_gA2X_j_N_gA2X_j_N)
    channel_link = (
        "https://www.youtube.com/@YouTubeCreators"  # Replace with your channel URL
    )

    # You can also ask the user for input
    # channel_link = input("Enter the YouTube channel URL: ")

    if channel_link:
        result_message = download_youtube_channel_as_mp4(channel_link, DOWNLOAD_DIR)
        print(result_message)
    else:
        print("No YouTube channel URL provided. Please enter a valid link.")

import argparse
import sys
import os
import yt_dlp

def search_and_get_info(query, max_results=5):
    """
    Searches YouTube using yt-dlp and extracts video info without downloading.
    
    Args:
        query (str): The search term.
        max_results (int): The number of search results to fetch.

    Returns:
        list: A list of tuples, where each tuple contains (video_id, video_title).
    """
    search_query = f"ytsearch{max_results}:{query}"
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True, # Significantly speeds up info extraction
        'force_generic_extractor': True,
    }
    
    videos = []
    print("   🔎 Searching for videos...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)
            
            if 'entries' in result and result['entries']:
                for entry in result['entries']:
                    # We check if 'id' and 'title' are present
                    if entry.get('id') and entry.get('title'):
                        videos.append((entry['id'], entry['title']))
            else:
                print("   ⚠️ No 'entries' found in search result.")

    except Exception as e:
        print(f"   ❌ An error occurred during search: {e}")
        
    return videos

def download_video_with_yt_dlp(video_id, path="."):
    """
    Downloads a YouTube video using its ID with yt-dlp.
    """
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    os.makedirs(path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(path, '%(title)s [%(id)s].%(ext)s'),
        'noplaylist': True,
    }

    print(f"   🔽 Queuing for download with yt-dlp...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"   ✅ Download finished for video ID: {video_id}")
    except Exception as e:
        print(f"   ❌ yt-dlp failed to download video {video_id}. Reason: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for and download YouTube videos using only yt-dlp (no API key required).")
    parser.add_argument("query", help="Search query/topic to find videos")
    parser.add_argument("-n", "--num-videos", type=int, default=3, help="Number of videos to find and download (default: 3)")
    parser.add_argument("-dp", "--download-path", default="./data", help="Directory to save downloaded videos (default: current directory)")

    args = parser.parse_args()
    print(f"🔍 Finding the top {args.num_videos} videos for query: '{args.query}'")
    videos_to_download = search_and_get_info(args.query, max_results=args.num_videos)
    
    if not videos_to_download:
        print("❌ No videos found for the given query. Exiting.")
        sys.exit(0)

    print(f"✅ Found {len(videos_to_download)} video(s). Starting downloads...")

    for vid, title in videos_to_download:
        print(f"\nProcessing video: '{title}' (ID: {vid})")
        download_video_with_yt_dlp(vid, path=args.download_path)
    
    print("\n✅ Download process complete.")
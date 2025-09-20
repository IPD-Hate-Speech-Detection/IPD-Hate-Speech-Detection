import requests
import pandas as pd
import argparse

def get_comments(video_id, api_key, max_pages=2):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": 100,
        "textFormat": "plainText"
    }
    
    comments = []
    page = 0
    
    while page < max_pages:
        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data:
            print(f"⚠️ Error fetching comments for {video_id}: {data}")
            break

        for item in data["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            text = comment["textDisplay"]
            author = comment["authorDisplayName"]
            likes = comment["likeCount"]
            published = comment["publishedAt"]

            comments.append({
                "Video ID": video_id,
                "Author": author,
                "Comment": text,
                "Likes": likes,
                "Published At": published
            })

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
            page += 1
        else:
            break
    
    return comments


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape YouTube video comments and save to CSV")
    parser.add_argument("api_key", help="YouTube Data API key")
    parser.add_argument("video_ids", nargs="+", help="One or more YouTube video IDs (space separated)")
    parser.add_argument("-o", "--output", default="youtube_comments.csv", help="Output CSV filename")
    parser.add_argument("-p", "--pages", type=int, default=5, help="Number of pages per video (100 comments per page)")
    
    args = parser.parse_args()
    
    all_comments = []
    for vid in args.video_ids:
        print(f"📥 Fetching comments for video: {vid}")
        all_comments.extend(get_comments(vid, args.api_key, max_pages=args.pages))
    
    if all_comments:
        df = pd.DataFrame(all_comments)
        df.to_csv(args.output, index=False, encoding="utf-8-sig")
        print(f"Saved {len(all_comments)} comments from {len(args.video_ids)} video(s) to {args.output}")
    else:
        print("No comments fetched.")

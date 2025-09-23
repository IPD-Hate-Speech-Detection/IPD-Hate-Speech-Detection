import praw
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import json

# --- SCRIPT CONFIGURATION ---

# 1. Load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
USER_AGENT = os.getenv("user_agent")

# 2. Define search parameters
config = json.load(open('config.json')) # Create a config file
# Use "OR" for multiple keywords
SEARCH_KEYWORDS = config.get('SEARCH_KEYWORDS', 'politics OR religion') 
# Use "all" to search across all of Reddit
SUBREDDIT_TO_SEARCH = config.get('SUBREDDIT_TO_SEARCH', 'politics') 
# How many posts to scrape
POST_LIMIT = config.get('POST_LIMIT', 5)           
# Can be "relevance", "hot", "top", "new", or "controversial"
SORT_BY = config.get('SORT_BY', 'controversial')      
# Can be "all", "day", "hour", "month", "week", "year"
TIME_FILTER = config.get('TIME_FILTER', 'month')          

# 3. NEW: Define the comment limit per post
# The maximum number of comments to scrape from each post
COMMENT_LIMIT = config.get('COMMENT_LIMIT', 50) 

# 4. Output file name
OUTPUT_CSV_FILE = config.get('OUTPUT_CSV_FILE', 'data/top_controversial_comments.csv')

# --- AUTHENTICATION & SCRAPING LOGIC ---

# Authenticate with Reddit
try:
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    print("✅ Successfully authenticated with Reddit.")
except Exception as e:
    print(f"❌ Error during authentication: {e}")
    exit()

# List to hold all comment data
all_comments_data = []
print(f"🔎 Searching for top {POST_LIMIT} '{SORT_BY}' posts in r/{SUBREDDIT_TO_SEARCH}...")

try:
    subreddit = reddit.subreddit(SUBREDDIT_TO_SEARCH)
    search_results = subreddit.search(
        SEARCH_KEYWORDS,
        sort=SORT_BY,
        time_filter=TIME_FILTER,
        limit=POST_LIMIT
    )

    # Loop through each post found
    for submission in search_results:
        print(f"\n Scraping post: '{submission.title}'")
        print(f" URL: {submission.url}")

        # --- MODIFICATION START ---

        # 1. SET THE COMMENT SORTING METHOD
        submission.comment_sort = "controversial" 

        # Reset comment counter for each new post
        comment_count = 0 
        
        # --- MODIFICATION END ---
        
        # It's still good practice to expand comments in case of nested replies
        submission.comments.replace_more(limit=0) # limit=0 is faster if we only want top-level

        # Iterate through comments
        for comment in submission.comments.list():
            # --- MODIFICATION START ---

            # 2. BREAK THE LOOP IF THE LIMIT IS REACHED
            if comment_count >= COMMENT_LIMIT:
                print(f"  -- Reached comment limit of {COMMENT_LIMIT}. Moving to next post. --")
                break
            
            # --- MODIFICATION END ---

            author_name = comment.author.name if comment.author else "[deleted]"
            
            all_comments_data.append({
                # 'post_title': submission.title,
                # 'post_url': submission.url,
                # 'author': author_name,
                'comment_body': comment.body,
                # 'score': comment.score,
                # 'created_utc': datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                # 'comment_id': comment.id,
                # 'permalink': f"https://www.reddit.com{comment.permalink}"
            })
            
            # Increment the counter
            comment_count += 1
            
    print(f"\nProcessed {len(all_comments_data)} total comments from the found posts.")

except Exception as e:
    print(f"❌ An error occurred during scraping: {e}")

# --- DATA EXPORT ---
if not all_comments_data:
    print("No data was scraped.")
else:
    df = pd.DataFrame(all_comments_data)
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
    print(f"\n✅ Success! All data saved to '{OUTPUT_CSV_FILE}'")
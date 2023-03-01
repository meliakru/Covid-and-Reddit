import csv
import praw
from datetime import datetime, timezone
reddit = praw.Reddit(client_id='OYjYY_r9i9haQK9wkw-3xw',
                     client_secret='BuYIA0kxVC5HOzSIEBPRnieUPj6Q4g',
                     user_agent='redScrapper') 

subredditName = 'depression'
subreddit = reddit.subreddit(subredditName)

# hot_posts_jan_2020 = subreddit.search('timestamp:1577836800..1580515200', sort='hot', limit=5)
start_timestamp = int(datetime(2020, 1, 1, tzinfo=timezone.utc).timestamp())
end_timestamp = int(datetime(2020, 2, 1, tzinfo=timezone.utc).timestamp())

top_posts = subreddit.top(limit=500)

filtered_posts = []

for post in top_posts:
    if start_timestamp <= post.created_utc <= end_timestamp:
        filtered_posts.append(post)

data = []
header = ['subReddit','Title', 'Content', 'Top Comment', 'upvotes','Number of comments', 'date', 'uniquePostID' ]

filtered_posts_5 = filtered_posts[:5]

for post in filtered_posts_5:
    title = post.title
    content = post.selftext
    top_comment = post.comments[0]
    initial_score = post.comments[0].score
    for comment in post.comments:
      if comment.score > initial_score:
            top_comment = comment 
            initial_score = comment.score
    top_comment_body = top_comment.body
    if top_comment.body:
      data.append([subredditName, title, content, top_comment.body, post.score, len(post.comments),post.created_utc, post.id])
    else:
      data.append([subredditName, title, content, "", post.score, len(post.comments), post.created_utc, post.id])

# write the data to a CSV file
with open(subredditName+'reddit_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)


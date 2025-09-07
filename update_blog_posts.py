#!/usr/bin/env python3
"""
Script to fetch latest blog posts from RSS feed and update README.md
For use with GitHub Actions to automatically update GitHub profile README
"""

import requests
import feedparser
import re
from datetime import datetime
from dateutil import parser as date_parser


def fetch_latest_blog_posts(rss_url, max_posts=5):
    """
    Fetch latest blog posts from RSS feed
    
    Args:
        rss_url (str): RSS feed URL
        max_posts (int): Maximum number of posts to fetch
        
    Returns:
        list: List of blog post dictionaries
    """
    try:
        # Fetch the RSS feed
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        # Parse the RSS feed
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print("No blog posts found in the feed")
            return []
        
        posts = []
        for entry in feed.entries[:max_posts]:
            # Parse published date
            published_date = "Unknown date"
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6]).strftime("%B %d, %Y")
            elif hasattr(entry, 'published'):
                try:
                    # Try to parse the published date string
                    parsed_date = date_parser.parse(entry.published)
                    published_date = parsed_date.strftime("%B %d, %Y")
                except:
                    published_date = entry.published
            
            # Get summary/description
            summary = ""
            if hasattr(entry, 'summary'):
                summary = entry.summary
            elif hasattr(entry, 'description'):
                summary = entry.description
            
            # Clean summary (remove HTML tags)
            if summary:
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary.replace('\n', ' ').strip()
                if len(summary) > 150:
                    summary = summary[:150] + "..."
            
            post = {
                'title': entry.title,
                'link': entry.link,
                'summary': summary,
                'published': published_date
            }
            posts.append(post)
            
        return posts
        
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return []
    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        return []


def update_readme_with_blog_posts(posts, readme_path='README.md'):
    """
    Update README.md with latest blog posts
    
    Args:
        posts (list): List of blog post dictionaries
        readme_path (str): Path to README.md file
    """
    try:
        # Read current README content
        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Create the blog posts section
        if posts:
            blog_section = "<!-- BLOG-POST-LIST:START -->\n"
            for post in posts:
                blog_section += f"- [{post['title']}]({post['link']}) - *{post['published']}*\n"
                if post['summary'].strip():
                    blog_section += f"  > {post['summary'].strip()}\n"
                blog_section += "\n"
            blog_section += "<!-- BLOG-POST-LIST:END -->"
        else:
            blog_section = "<!-- BLOG-POST-LIST:START -->\n"
            blog_section += "- No blog posts available at the moment.\n"
            blog_section += "<!-- BLOG-POST-LIST:END -->"
        
        # Replace the blog posts section
        pattern = r'<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->'
        updated_content = re.sub(pattern, blog_section, content, flags=re.DOTALL)
        
        # If the pattern wasn't found, add the blog section after a specific marker
        if content == updated_content:
            print("Blog post markers not found. Adding blog section...")
            # Look for a suitable place to add the blog section
            if "## Latest Blog Posts" in content:
                updated_content = re.sub(
                    r'(## Latest Blog Posts.*?)\n',
                    f'\\1\n\n{blog_section}\n',
                    content,
                    flags=re.DOTALL
                )
            else:
                # Add at the end
                updated_content = content + f"\n\n## Latest Blog Posts\n\n{blog_section}\n"
        
        # Write updated content back to README
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"Successfully updated README.md with {len(posts)} blog posts")
        
    except FileNotFoundError:
        print(f"README.md file not found at {readme_path}")
    except Exception as e:
        print(f"Error updating README: {e}")


def main():
    """Main function"""
    print("🚀 Starting blog posts update...")
    
    # Your blog RSS feed URL
    RSS_URL = "https://blog.shrivarshapoojary.in/index.xml"
    
    # Fetch latest blog posts
    posts = fetch_latest_blog_posts(RSS_URL, max_posts=5)
    
    if posts:
        print(f"📖 Found {len(posts)} blog posts")
        for i, post in enumerate(posts, 1):
            print(f"  {i}. {post['title']} ({post['published']})")
    else:
        print("❌ No blog posts found")
    
    # Update README
    update_readme_with_blog_posts(posts)
    
    print("✅ Blog posts update completed!")


if __name__ == "__main__":
    main()

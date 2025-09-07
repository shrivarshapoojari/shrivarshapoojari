#!/usr/bin/env python3
"""
Simple script to fetch latest blog posts from RSS feed and update README.md
Uses only requests library (no external dependencies)
"""

import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime


def fetch_latest_blog_posts(rss_url, max_posts=5):
    """
    Fetch latest blog posts from RSS feed using only requests and xml.etree
    """
    try:
        # Fetch the RSS feed
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Find all items
        items = root.findall('.//item')
        
        if not items:
            print("No blog posts found in the feed")
            return []
        
        posts = []
        for item in items[:max_posts]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            description_elem = item.find('description')
            
            if title_elem is not None and link_elem is not None:
                # Get title and link
                title = title_elem.text.strip() if title_elem.text else 'No Title'
                link = link_elem.text.strip() if link_elem.text else ''
                
                # Parse date
                published_date = "Unknown date"
                if pub_date_elem is not None and pub_date_elem.text:
                    try:
                        # Try to parse RFC 2822 date format (typical for RSS)
                        date_str = pub_date_elem.text.strip()
                        # Remove timezone info for parsing (keep it simple)
                        if '+' in date_str:
                            date_str = date_str.split('+')[0].strip()
                        elif ' GMT' in date_str:
                            date_str = date_str.replace(' GMT', '').strip()
                        elif ' UTC' in date_str:
                            date_str = date_str.replace(' UTC', '').strip()
                        
                        # Try to parse common date formats
                        for fmt in ['%a, %d %b %Y %H:%M:%S', '%d %b %Y %H:%M:%S', '%a, %d %b %Y']:
                            try:
                                parsed_date = datetime.strptime(date_str, fmt)
                                published_date = parsed_date.strftime("%B %d, %Y")
                                break
                            except ValueError:
                                continue
                        
                        # If all parsing fails, use original date
                        if published_date == "Unknown date":
                            published_date = pub_date_elem.text.strip()
                            
                    except Exception:
                        published_date = pub_date_elem.text.strip() if pub_date_elem.text else "Unknown date"
                
                # Get description/summary
                summary = ""
                if description_elem is not None and description_elem.text:
                    summary = description_elem.text.strip()
                    # Clean HTML tags
                    summary = re.sub(r'<[^>]+>', '', summary)
                    summary = summary.replace('\n', ' ').strip()
                    if len(summary) > 150:
                        summary = summary[:150] + "..."
                
                post = {
                    'title': title,
                    'link': link,
                    'summary': summary,
                    'published': published_date
                }
                posts.append(post)
                
        return posts
        
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except Exception as e:
        print(f"Error processing feed: {e}")
        return []


def update_readme_with_blog_posts(posts, readme_path='README.md'):
    """
    Update README.md with latest blog posts
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
        
        # Check if replacement was successful
        if content == updated_content:
            print("Warning: Blog post markers not found in README.md")
            return False
        
        # Write updated content back to README
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"Successfully updated README.md with {len(posts)} blog posts")
        return True
        
    except FileNotFoundError:
        print(f"README.md file not found at {readme_path}")
        return False
    except Exception as e:
        print(f"Error updating README: {e}")
        return False


def main():
    """Main function"""
    print("🚀 Starting blog posts update...")
    
    # Your blog RSS feed URL
    RSS_URL = "https://blog.shrivarshapoojary.in/index.xml"
    
    # Fetch latest blog posts
    posts = fetch_latest_blog_posts(RSS_URL, max_posts=5)
    
    if posts:
        print(f"📖 Found {len(posts)} blog posts:")
        for i, post in enumerate(posts, 1):
            print(f"  {i}. {post['title']} ({post['published']})")
        
        # Update README
        success = update_readme_with_blog_posts(posts)
        
        if success:
            print("✅ Blog posts updated in README.md successfully!")
        else:
            print("❌ Failed to update README.md")
    else:
        print("❌ No blog posts found")
    
    print("✅ Blog posts update completed!")


if __name__ == "__main__":
    main()

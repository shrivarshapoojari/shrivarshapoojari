# Auto-Update Blog Posts in GitHub Profile README

This repository contains the setup to automatically fetch and display your latest blog posts from your RSS feed in your GitHub profile README.

## 🚀 Features

- ✅ Automatically fetches latest blog posts from your RSS feed
- ✅ Updates GitHub profile README with blog post titles, links, and dates
- ✅ Includes blog post summaries/descriptions
- ✅ Runs automatically via GitHub Actions (daily)
- ✅ Can be triggered manually
- ✅ No external dependencies (uses only Python standard library + requests)

## 📁 Files Overview

### Scripts
- `update_blog_simple.py` - Main script that fetches RSS feed and updates README
- `update_blog_posts.py` - Alternative version using feedparser library
- `test_rss.py` - Simple test script to verify RSS feed accessibility

### GitHub Actions
- `.github/workflows/update-blog-posts.yml` - Automated workflow that runs daily

### Dependencies
- `requirements.txt` - Python package dependencies

## 🛠️ Setup Instructions

### 1. Repository Setup
Make sure your repository is named exactly as your GitHub username (e.g., `shrivarshapoojari/shrivarshapoojari`).

### 2. README Markers
Your README.md must contain the following markers where blog posts will be inserted:

```markdown
## 📝 Latest Blog Posts
<!-- BLOG-POST-LIST:START -->
<!-- BLOG-POST-LIST:END -->
```

### 3. Configure RSS URL
In `update_blog_simple.py`, update the RSS_URL variable with your blog's RSS feed:

```python
RSS_URL = "https://blog.shrivarshapoojary.in/index.xml"
```

### 4. Manual Testing
Test the script locally:

```bash
python update_blog_simple.py
```

### 5. GitHub Actions
The workflow will run automatically:
- **Daily**: Every day at 6:00 AM UTC
- **On Push**: When you push to the main branch
- **Manual**: You can trigger it manually from the Actions tab

## 📅 Automation Schedule

The GitHub Action runs:
- Every day at 6:00 AM UTC
- On every push to main branch
- Can be triggered manually from GitHub Actions tab

## 🔧 Customization

### Change Number of Posts
Modify the `max_posts` parameter in the script:

```python
posts = fetch_latest_blog_posts(RSS_URL, max_posts=5)  # Change 5 to desired number
```

### Modify Date Format
Update the date formatting in the `fetch_latest_blog_posts` function:

```python
published_date = parsed_date.strftime("%B %d, %Y")  # Change format as needed
```

### Customize Post Format
Modify the blog section creation in `update_readme_with_blog_posts` function:

```python
blog_section += f"- [{post['title']}]({post['link']}) - *{post['published']}*\n"
```

## 🐛 Troubleshooting

### RSS Feed Issues
1. Test your RSS feed URL in a browser
2. Run `python test_rss.py` to check accessibility
3. Ensure RSS feed is publicly accessible

### GitHub Actions Not Working
1. Check the Actions tab for error logs
2. Verify repository permissions
3. Ensure the workflow file is in `.github/workflows/`

### Blog Posts Not Appearing
1. Check if README has the correct markers
2. Verify the RSS feed contains posts
3. Check for XML parsing errors in action logs

## 📊 Sample Output

The script will update your README with something like:

```markdown
## 📝 Latest Blog Posts
<!-- BLOG-POST-LIST:START -->
- [WebAssembly: Near-Native Performance in the Browser](https://blog.shrivarshapoojary.in/posts/webassembly/) - *September 04, 2025*
  > WebAssembly (WASM) is a game-changer for web development...

- [CAP Theorem: The Fundamental Trade-off in Distributed Systems](https://blog.shrivarshapoojary.in/posts/cap-theorem/) - *September 03, 2025*
  > In distributed systems, you can't have your cake and eat it too...

<!-- BLOG-POST-LIST:END -->
```

## 🔄 Manual Update

To manually update blog posts:

1. Go to your repository's Actions tab
2. Click on "Update Blog Posts" workflow
3. Click "Run workflow"
4. Select the main branch and click "Run workflow"

## 📝 Notes

- The script respects GitHub's rate limits
- Blog post summaries are truncated to 150 characters
- HTML tags are stripped from descriptions
- Dates are formatted in a readable format
- The script handles various RSS date formats

## 🤝 Contributing

Feel free to improve the script or add new features! Some ideas:
- Add support for more RSS formats
- Include author information
- Add tags/categories
- Implement caching to avoid unnecessary updates

---

**Happy blogging!** 🎉

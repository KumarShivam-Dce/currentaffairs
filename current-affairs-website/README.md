# 📚 Daily Current Affairs Website - Complete Setup Guide

## 🎯 What This Project Does

This is a **100% FREE** current affairs website that:
- ✅ Updates **automatically every day** using GitHub Actions
- ✅ Fetches news from free RSS feeds (PIB, The Hindu, etc.)
- ✅ Filters only **exam-relevant** content
- ✅ Saves data **permanently** by date/month/year
- ✅ Works entirely on **GitHub Pages** (no hosting costs)
- ✅ Provides topic-wise filtering and search
- ✅ Mobile-friendly, fast, and clean UI

---

## 📁 Project Structure

```
current-affairs-website/
├── index.html              # Main website
├── style.css              # Styling
├── app.js                 # Frontend logic
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── .github/
│   └── workflows/
│       └── update-news.yml  # Daily automation
├── scripts/
│   └── fetch_news.py      # News fetcher
├── config/
│   └── rss_feeds.json     # RSS feed sources
└── data/
    └── current-affairs/
        └── 2025/
            └── January/
                └── 2025-01-15.md  # Daily news file
```

---

## 🚀 Step-by-Step Setup (For Absolute Beginners)

### Step 1: Create GitHub Account
1. Go to https://github.com
2. Sign up for free (if you don't have an account)

### Step 2: Create New Repository
1. Click **"New"** button (green button on GitHub homepage)
2. Repository name: `current-affairs-website`
3. Set to **Public**
4. ✅ Check "Add a README file"
5. Click **"Create repository"**

### Step 3: Upload Project Files

**Option A: Using GitHub Web Interface (Easiest)**
1. Click **"Add file"** → **"Upload files"**
2. Drag and drop ALL files from this project
3. Make sure to maintain the folder structure
4. Click **"Commit changes"**

**Option B: Using Git Commands (If you know Git)**
```bash
git clone https://github.com/YOUR-USERNAME/current-affairs-website.git
cd current-affairs-website
# Copy all project files here
git add .
git commit -m "Initial commit"
git push
```

### Step 4: Enable GitHub Pages
1. Go to repository **Settings**
2. Scroll to **"Pages"** section (left sidebar)
3. Under **"Source"**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **"Save"**
5. Wait 2-3 minutes
6. Your website will be live at: `https://YOUR-USERNAME.github.io/current-affairs-website/`

### Step 5: Enable GitHub Actions
1. Go to **"Actions"** tab in your repository
2. Click **"I understand my workflows, enable them"**
3. The automation is now active!

### Step 6: Test Manual Run (Optional)
1. Go to **"Actions"** tab
2. Click on **"Daily Current Affairs Update"** workflow
3. Click **"Run workflow"** button
4. Select `main` branch
5. Click green **"Run workflow"** button
6. Wait for it to complete (takes 30-60 seconds)
7. Check `data/current-affairs/` folder for new files

---

## ⚙️ How Automation Works

### Daily Schedule
- Runs every day at **6:00 AM IST** (12:30 AM UTC)
- Automatically fetches latest news
- Filters exam-relevant content
- Saves to date-wise markdown files
- Commits changes to repository
- Website updates automatically

### Manual Trigger
You can also run it manually anytime:
1. Go to **Actions** → **Daily Current Affairs Update**
2. Click **"Run workflow"**

---

## 📝 Data Storage Format

News is saved in markdown files organized by date:

```
data/current-affairs/
├── 2025/
│   ├── January/
│   │   ├── 2025-01-01.md
│   │   ├── 2025-01-02.md
│   │   └── 2025-01-03.md
│   ├── February/
│   └── March/
├── 2024/
│   └── December/
```

### Each File Contains:
```markdown
# Current Affairs - 15 January 2025

## RBI Announces New Monetary Policy

**Category:** Economy

Reserve Bank of India ne repo rate 6.5% pe maintain rakha hai...

**Exam Angle:** Monetary policy tools aur RBI ke functions yaad rakhna

**Static Link:** RBI official website pe policy documents check karo

---

## New Defence Exercise with USA

**Category:** Defence

India aur USA ke beech 'Yudh Abhyas' exercise start hua...

**Exam Angle:** Bilateral exercises ka naam aur partner country yaad rakhna

**Static Link:** Defence Ministry annual report useful hai

---
```

---

## 🎨 Customization Options

### Change Update Time
Edit `.github/workflows/update-news.yml`:
```yaml
schedule:
  - cron: '30 0 * * *'  # Change this (currently 6 AM IST)
```

Cron format: `minute hour day month weekday`
- `0 12 * * *` = 5:30 PM IST (12:00 PM UTC)
- `30 6 * * *` = 12:00 PM IST (6:30 AM UTC)

### Add More RSS Feeds
Edit `scripts/fetch_news.py` in the `RSS_FEEDS` list:
```python
RSS_FEEDS = [
    {'url': 'https://example.com/rss', 'name': 'Source Name'},
    # Add more feeds here
]
```

### Change Categories
Edit `RELEVANT_KEYWORDS` dictionary in `fetch_news.py`

### Modify UI Colors
Edit `style.css`:
```css
/* Change primary color */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## 🔧 Troubleshooting

### Issue 1: Website Not Loading
**Solution:**
- Wait 5 minutes after enabling GitHub Pages
- Check if repository is Public (not Private)
- Verify URL: `https://YOUR-USERNAME.github.io/REPO-NAME/`

### Issue 2: No News Appearing
**Solution:**
- Run workflow manually from Actions tab
- Check if `data/current-affairs/` folder has files
- Look at workflow logs for errors

### Issue 3: Workflow Not Running
**Solution:**
- Go to Actions → Enable workflows if disabled
- Check if schedule is correct in `update-news.yml`
- Verify repository has write permissions

### Issue 4: Python Errors
**Solution:**
- Check `requirements.txt` is uploaded
- Verify Python version in workflow (should be 3.10)
- Look at error logs in Actions tab

---

## 💡 Pro Tips

1. **First Time Setup**: Manually run the workflow once to populate initial data
2. **Backup**: GitHub automatically keeps all old commits (version history)
3. **Mobile Access**: Website works perfectly on phones
4. **Sharing**: Share your website URL with friends
5. **Updates**: Pull latest changes from this repo periodically

---

## 📊 Features Overview

| Feature | Status |
|---------|--------|
| Auto-updates daily | ✅ |
| 100% Free | ✅ |
| Permanent storage | ✅ |
| Topic filtering | ✅ |
| Search functionality | ✅ |
| Mobile responsive | ✅ |
| Date navigation | ✅ |
| Year/Month filters | ✅ |
| Exam-focused content | ✅ |
| Hinglish language | ✅ |

---

## 🎓 Content Categories

- **Polity**: Constitution, Supreme Court, Acts, Bills
- **Economy**: RBI, GDP, Budget, Fiscal Policy
- **Government Schemes**: Yojanas, Missions, Initiatives
- **Defence**: Military Exercises, Defence Deals
- **International Relations**: Treaties, Summits, Agreements
- **Science & Technology**: ISRO, DRDO, Innovation
- **Reports & Indices**: Rankings, Surveys, Data
- **Environment**: Climate, Conservation, Green Energy

---

## 📞 Support

If you face any issues:
1. Check the troubleshooting section above
2. Look at GitHub Actions logs for detailed errors
3. Verify all files are uploaded correctly
4. Make sure repository is Public

---

## 🌟 Benefits

✅ **Zero Cost**: No hosting fees, no API costs  
✅ **Automated**: Set it and forget it  
✅ **Permanent**: All data saved forever  
✅ **Accessible**: Access from anywhere  
✅ **Searchable**: Find any topic/date instantly  
✅ **Exam-Ready**: Filtered for competitive exams  
✅ **Fast**: Lightweight, loads in seconds  
✅ **Open Source**: Fully customizable  

---

## 📜 License

Free to use for everyone. No restrictions.

---

## 🙏 Acknowledgments

- RSS feeds from PIB, The Hindu, Indian Express, UN
- GitHub for free hosting and automation
- Python feedparser library

---

**Made with ❤️ for exam aspirants**

**Star ⭐ this repository if you find it helpful!**

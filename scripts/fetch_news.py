#!/usr/bin/env python3
"""
Daily Current Affairs Fetcher
Fetches news from RSS feeds, filters exam-relevant content, and saves to markdown files
"""

import feedparser
import json
import os
from datetime import datetime
import re
from pathlib import Path

# Exam-relevant keywords for filtering
RELEVANT_KEYWORDS = {
    'polity': ['supreme court', 'constitution', 'parliament', 'bill', 'act', 'amendment', 'judiciary', 'legislation', 'lok sabha', 'rajya sabha', 'article', 'governor', 'president'],
    'economy': ['rbi', 'reserve bank', 'gdp', 'inflation', 'fiscal', 'monetary', 'budget', 'gst', 'tax', 'economy', 'economic', 'finance', 'rupee', 'repo rate', 'bank', 'sebi', 'stock market'],
    'schemes': ['yojana', 'scheme', 'mission', 'abhiyan', 'portal', 'programme', 'initiative', 'ministry launched'],
    'defence': ['army', 'navy', 'air force', 'defence', 'exercise', 'missile', 'drdo', 'isro', 'military', 'security', 'border'],
    'international': ['treaty', 'agreement', 'bilateral', 'summit', 'united nations', 'un', 'world bank', 'imf', 'foreign policy', 'external affairs', 'g20', 'brics', 'saarc'],
    'science': ['isro', 'space', 'satellite', 'rocket', 'research', 'technology', 'innovation', 'ai', 'artificial intelligence', 'cyber', 'digital', 'electronics'],
    'reports': ['index', 'report', 'ranking', 'survey', 'study', 'data', 'statistics', 'released by'],
    'environment': ['environment', 'climate', 'pollution', 'wildlife', 'forest', 'conservation', 'renewable', 'solar', 'emission', 'green', 'sustainable']
}

# Keywords to reject (non-exam content)
REJECT_KEYWORDS = ['murder', 'rape', 'crime', 'arrest', 'controversy', 'scandal', 'opinion:', 'bollywood', 'cricket', 'entertainment', 'horoscope']

# RSS Feeds (all free sources)
RSS_FEEDS = [
    {'url': 'https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1', 'name': 'PIB India'},
    {'url': 'https://www.thehindu.com/news/national/?service=rss', 'name': 'The Hindu National'},
    {'url': 'https://indianexpress.com/section/india/feed/', 'name': 'Indian Express'},
    {'url': 'https://www.un.org/en/rss/news.xml', 'name': 'UN News'},
]

def categorize_news(title, description):
    """Categorize news based on keywords"""
    text = (title + ' ' + description).lower()
    
    for category, keywords in RELEVANT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                if category == 'polity':
                    return 'Polity'
                elif category == 'economy':
                    return 'Economy'
                elif category == 'schemes':
                    return 'Government Schemes'
                elif category == 'defence':
                    return 'Defence'
                elif category == 'international':
                    return 'International Relations'
                elif category == 'science':
                    return 'Science & Technology'
                elif category == 'reports':
                    return 'Reports & Indices'
                elif category == 'environment':
                    return 'Environment'
    
    return None

def is_relevant(title, description):
    """Check if news is exam-relevant"""
    text = (title + ' ' + description).lower()
    
    # Reject based on keywords
    for reject_word in REJECT_KEYWORDS:
        if reject_word in text:
            return False
    
    # Accept if matches any relevant keyword
    for keywords in RELEVANT_KEYWORDS.values():
        for keyword in keywords:
            if keyword in text:
                return True
    
    return False

def clean_text(text):
    """Clean and format text"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    return text.strip()

def generate_exam_angle(category, title):
    """Generate exam angle based on category"""
    angles = {
        'Polity': 'Constitutional provisions, judicial precedents, legislative procedures se related hai',
        'Economy': 'Economic indicators, monetary policy, fiscal measures ke liye important',
        'Government Schemes': 'Scheme objectives, beneficiaries, implementation ministry yaad rakhna',
        'Defence': 'Defence partnerships, exercises ka naam, equipment specifications note karna',
        'International Relations': 'Bilateral/multilateral agreements, international organizations yaad rakhna',
        'Science & Technology': 'Applications, organizations (ISRO/DRDO), launches ki dates important hai',
        'Reports & Indices': 'India ki ranking, report publisher, key findings note karna',
        'Environment': 'International conventions, conservation efforts, targets yaad rakhna'
    }
    
    return angles.get(category, 'Static GK ke liye relevant hai')

def get_static_link(category):
    """Generate static link suggestions"""
    links = {
        'Polity': 'Constitution ki related articles check karo',
        'Economy': 'Economic Survey aur Budget documents dekho',
        'Government Schemes': 'Ministry website pe scheme details available hai',
        'Defence': 'Defence Ministry annual report useful hai',
        'International Relations': 'MEA website pe treaties aur agreements listed hai',
        'Science & Technology': 'ISRO/DRDO official websites check karo',
        'Reports & Indices': 'Report publisher ki official website dekho',
        'Environment': 'Ministry of Environment notifications track karo'
    }
    
    return links.get(category, 'Related government portal check karo')

def summarize_content(title, description):
    """Create brief 1-2 line summary"""
    desc = clean_text(description)
    
    # Take first 2 sentences or 150 characters
    sentences = desc.split('.')
    if len(sentences) > 0:
        summary = '. '.join(sentences[:2])
        if len(summary) > 200:
            summary = summary[:200] + '...'
        return summary
    
    return desc[:150] + '...' if len(desc) > 150 else desc

def fetch_and_process_news():
    """Main function to fetch and process news"""
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    year = today.strftime('%Y')
    month = today.strftime('%B')
    
    # Create directory structure
    output_dir = Path(f'data/current-affairs/{year}/{month}')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'{date_str}.md'
    
    # If file already exists, append to it
    if output_file.exists():
        print(f"File {output_file} already exists. Appending new content...")
        mode = 'a'
    else:
        mode = 'w'
    
    news_items = []
    
    print("Fetching news from RSS feeds...")
    
    for feed_info in RSS_FEEDS:
        try:
            print(f"Processing {feed_info['name']}...")
            feed = feedparser.parse(feed_info['url'])
            
            for entry in feed.entries[:10]:  # Top 10 from each feed
                title = clean_text(entry.get('title', ''))
                description = clean_text(entry.get('description', '') or entry.get('summary', ''))
                
                if not title:
                    continue
                
                # Check relevance
                if is_relevant(title, description):
                    category = categorize_news(title, description)
                    
                    if category:
                        news_items.append({
                            'title': title,
                            'description': description,
                            'category': category,
                            'source': feed_info['name']
                        })
        
        except Exception as e:
            print(f"Error processing {feed_info['name']}: {str(e)}")
            continue
    
    print(f"Found {len(news_items)} relevant news items")
    
    # Remove duplicates based on title similarity
    unique_items = []
    seen_titles = set()
    
    for item in news_items:
        # Create a simplified version of title for comparison
        simple_title = re.sub(r'[^a-z0-9]', '', item['title'].lower())[:50]
        
        if simple_title not in seen_titles:
            seen_titles.add(simple_title)
            unique_items.append(item)
    
    print(f"After removing duplicates: {len(unique_items)} items")
    
    # Write to markdown file
    with open(output_file, mode, encoding='utf-8') as f:
        if mode == 'w':
            f.write(f"# Current Affairs - {today.strftime('%d %B %Y')}\n\n")
        
        for item in unique_items:
            f.write(f"## {item['title']}\n\n")
            f.write(f"**Category:** {item['category']}\n\n")
            
            summary = summarize_content(item['title'], item['description'])
            f.write(f"{summary}\n\n")
            
            exam_angle = generate_exam_angle(item['category'], item['title'])
            f.write(f"**Exam Angle:** {exam_angle}\n\n")
            
            static_link = get_static_link(item['category'])
            f.write(f"**Static Link:** {static_link}\n\n")
            
            f.write("---\n\n")
    
    print(f"✅ News saved to {output_file}")
    return len(unique_items)

if __name__ == '__main__':
    try:
        count = fetch_and_process_news()
        print(f"Successfully processed {count} news items!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

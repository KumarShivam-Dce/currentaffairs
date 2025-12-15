// Global variables
let allNewsData = [];
let filteredData = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadNewsData();
    setupEventListeners();
});

// Setup event listeners for filters
function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', applyFilters);
    document.getElementById('yearFilter').addEventListener('change', applyFilters);
    document.getElementById('monthFilter').addEventListener('change', applyFilters);
    document.getElementById('topicFilter').addEventListener('change', applyFilters);
}

// Load news data from GitHub repository
async function loadNewsData() {
    const loading = document.getElementById('loading');
    const noData = document.getElementById('noData');
    const container = document.getElementById('contentContainer');
    
    try {
        // Get repository info from current URL
        const repoOwner = getRepoOwner();
        const repoName = getRepoName();
        
        // Fetch directory structure
        const years = await fetchYears(repoOwner, repoName);
        
        if (years.length === 0) {
            loading.style.display = 'none';
            noData.style.display = 'block';
            return;
        }
        
        // Populate year filter
        populateYearFilter(years);
        
        // Load all news files
        for (const year of years) {
            const months = await fetchMonths(repoOwner, repoName, year);
            for (const month of months) {
                const files = await fetchFiles(repoOwner, repoName, year, month);
                for (const file of files) {
                    const content = await fetchFileContent(repoOwner, repoName, year, month, file);
                    const newsData = parseMarkdown(content, year, month, file);
                    allNewsData.push(...newsData);
                }
            }
        }
        
        // Sort by date (newest first)
        allNewsData.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        loading.style.display = 'none';
        
        if (allNewsData.length === 0) {
            noData.style.display = 'block';
        } else {
            filteredData = [...allNewsData];
            displayNews();
        }
        
    } catch (error) {
        console.error('Error loading news:', error);
        loading.style.display = 'none';
        noData.style.display = 'block';
    }
}

// Get repository owner from URL
function getRepoOwner() {
    // For GitHub Pages: username.github.io
    const hostname = window.location.hostname;
    return hostname.split('.')[0];
}

// Get repository name from URL
function getRepoName() {
    // For project pages: username.github.io/repo-name
    const pathname = window.location.pathname;
    const parts = pathname.split('/').filter(p => p);
    return parts.length > 0 ? parts[0] : 'current-affairs-website';
}

// Fetch years from repository
async function fetchYears(owner, repo) {
    try {
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/data/current-affairs`);
        const data = await response.json();
        return data.filter(item => item.type === 'dir').map(item => item.name);
    } catch (error) {
        console.error('Error fetching years:', error);
        return [];
    }
}

// Fetch months for a given year
async function fetchMonths(owner, repo, year) {
    try {
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/data/current-affairs/${year}`);
        const data = await response.json();
        return data.filter(item => item.type === 'dir').map(item => item.name);
    } catch (error) {
        console.error('Error fetching months:', error);
        return [];
    }
}

// Fetch files for a given year and month
async function fetchFiles(owner, repo, year, month) {
    try {
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/data/current-affairs/${year}/${month}`);
        const data = await response.json();
        return data.filter(item => item.type === 'file' && item.name.endsWith('.md')).map(item => item.name);
    } catch (error) {
        console.error('Error fetching files:', error);
        return [];
    }
}

// Fetch content of a specific file
async function fetchFileContent(owner, repo, year, month, filename) {
    try {
        const response = await fetch(`https://raw.githubusercontent.com/${owner}/${repo}/main/data/current-affairs/${year}/${month}/${filename}`);
        return await response.text();
    } catch (error) {
        console.error('Error fetching file content:', error);
        return '';
    }
}

// Parse markdown content
function parseMarkdown(content, year, month, filename) {
    const date = filename.replace('.md', '');
    const lines = content.split('\n');
    const newsItems = [];
    let currentItem = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.startsWith('## ')) {
            // Save previous item
            if (currentItem) {
                newsItems.push(currentItem);
            }
            // Start new item
            currentItem = {
                date: date,
                year: year,
                month: month,
                headline: line.replace('## ', ''),
                content: '',
                category: '',
                examAngle: '',
                staticLink: ''
            };
        } else if (line.startsWith('**Category:**')) {
            if (currentItem) {
                currentItem.category = line.replace('**Category:**', '').trim();
            }
        } else if (line.startsWith('**Exam Angle:**')) {
            if (currentItem) {
                currentItem.examAngle = line.replace('**Exam Angle:**', '').trim();
            }
        } else if (line.startsWith('**Static Link:**')) {
            if (currentItem) {
                currentItem.staticLink = line.replace('**Static Link:**', '').trim();
            }
        } else if (line && currentItem && !line.startsWith('**')) {
            currentItem.content += line + ' ';
        }
    }
    
    // Add last item
    if (currentItem) {
        newsItems.push(currentItem);
    }
    
    return newsItems;
}

// Populate year filter dropdown
function populateYearFilter(years) {
    const yearFilter = document.getElementById('yearFilter');
    years.sort().reverse().forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });
}

// Apply filters
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const yearFilter = document.getElementById('yearFilter').value;
    const monthFilter = document.getElementById('monthFilter').value;
    const topicFilter = document.getElementById('topicFilter').value;
    
    filteredData = allNewsData.filter(item => {
        const matchesSearch = !searchTerm || 
            item.headline.toLowerCase().includes(searchTerm) ||
            item.content.toLowerCase().includes(searchTerm) ||
            item.category.toLowerCase().includes(searchTerm);
        
        const matchesYear = !yearFilter || item.year === yearFilter;
        const matchesMonth = !monthFilter || item.month === monthFilter;
        const matchesTopic = !topicFilter || item.category.includes(topicFilter);
        
        return matchesSearch && matchesYear && matchesMonth && matchesTopic;
    });
    
    displayNews();
}

// Display news items
function displayNews() {
    const container = document.getElementById('contentContainer');
    container.innerHTML = '';
    
    if (filteredData.length === 0) {
        container.innerHTML = '<div class="no-data"><h3>No results found</h3><p>Try adjusting your filters</p></div>';
        return;
    }
    
    // Group by date
    const groupedByDate = {};
    filteredData.forEach(item => {
        if (!groupedByDate[item.date]) {
            groupedByDate[item.date] = [];
        }
        groupedByDate[item.date].push(item);
    });
    
    // Display each date section
    Object.keys(groupedByDate).sort().reverse().forEach(date => {
        const section = createDateSection(date, groupedByDate[date]);
        container.appendChild(section);
    });
}

// Create date section element
function createDateSection(date, items) {
    const section = document.createElement('div');
    section.className = 'date-section';
    
    const header = document.createElement('div');
    header.className = 'date-header';
    
    const dateObj = new Date(date);
    const formattedDate = dateObj.toLocaleDateString('en-IN', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    header.innerHTML = `
        <div class="date-title">${formattedDate}</div>
        <div class="date-info">${items.length} news items</div>
    `;
    
    section.appendChild(header);
    
    items.forEach(item => {
        const newsItem = createNewsItem(item);
        section.appendChild(newsItem);
    });
    
    return section;
}

// Create news item element
function createNewsItem(item) {
    const div = document.createElement('div');
    div.className = 'news-item';
    
    let html = '';
    
    if (item.category) {
        html += `<div class="news-category">${item.category}</div>`;
    }
    
    html += `<div class="news-headline">${item.headline}</div>`;
    
    if (item.content) {
        html += `<div class="news-content">${item.content.trim()}</div>`;
    }
    
    if (item.examAngle) {
        html += `<div class="exam-angle"><strong>Exam Angle:</strong> ${item.examAngle}</div>`;
    }
    
    if (item.staticLink) {
        html += `<div class="static-link"><strong>Static Link:</strong> ${item.staticLink}</div>`;
    }
    
    div.innerHTML = html;
    return div;
}

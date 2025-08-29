// Search functionality for CSES Problem Collection
class ProblemSearch {
    constructor() {
        this.searchInput = null;
        this.searchResults = null;
        this.allProblems = [];
        this.init();
    }

    init() {
        if (!this.createSearchUI()) {
            console.error('Failed to initialize search UI');
            return;
        }
        this.loadProblems();
        this.bindEvents();
    }

    createSearchUI() {
        // Search UI is already in the HTML, just get references
        this.searchInput = document.getElementById('problem-search');
        this.searchResults = document.getElementById('search-results');
        
        if (!this.searchInput || !this.searchResults) {
            console.error('Search elements not found');
            return false;
        }
        
        console.log('Search UI found successfully');
        return true;
    }

    loadProblems() {
        // Extract problems from the navigation structure
        const problemLinks = document.querySelectorAll('.sidebar a[href*="/problem_soulutions/"], .sidebar.sticky a[href*="/problem_soulutions/"]');
        
        console.log('Found problem links:', problemLinks.length);
        
        problemLinks.forEach(link => {
            const title = link.textContent.trim();
            const url = link.href;
            
            // Skip summary pages and category pages
            if (title === 'Summary' || !url.includes('_analysis')) {
                return;
            }

            // Extract difficulty from title (stars)
            const difficultyMatch = title.match(/^(⭐+)\s/);
            const difficulty = difficultyMatch ? difficultyMatch[1].length : 0;
            const cleanTitle = title.replace(/^⭐+\s/, '');

            // Extract category from URL
            const categoryMatch = url.match(/problem_soulutions\/([^\/]+)/);
            const category = categoryMatch ? this.formatCategory(categoryMatch[1]) : '';

            this.allProblems.push({
                title: cleanTitle,
                fullTitle: title,
                url: url,
                difficulty: difficulty,
                category: category,
                searchText: `${cleanTitle} ${category} ${this.getDifficultyText(difficulty)}`.toLowerCase()
            });
        });
        
        console.log('Loaded problems:', this.allProblems.length);
    }

    formatCategory(category) {
        return category
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    getDifficultyText(difficulty) {
        const difficulties = ['', 'Easy', 'Medium', 'Hard', 'Very Hard'];
        return difficulties[difficulty] || '';
    }

    bindEvents() {
        // Search input event
        this.searchInput.addEventListener('input', (e) => {
            this.performSearch(e.target.value);
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.performSearch(this.searchInput.value);
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.searchInput.focus();
            }
            if (e.key === 'Escape') {
                this.clearSearch();
            }
        });

        // Click outside to close results
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.hideResults();
            }
        });
    }

    performSearch(query) {
        const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
        
        if (!query.trim()) {
            this.hideResults();
            return;
        }

        const results = this.allProblems.filter(problem => {
            const matchesQuery = problem.searchText.includes(query.toLowerCase());
            const matchesFilter = activeFilter === 'all' || problem.difficulty.toString() === activeFilter;
            return matchesQuery && matchesFilter;
        });

        this.displayResults(results, query);
    }

    displayResults(results, query) {
        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="no-results">
                    <p>No problems found for "${query}"</p>
                    <p>Try a different search term or check the filters</p>
                </div>
            `;
        } else {
            const resultsHtml = results.map(problem => `
                <a href="${problem.url}" class="search-result-item">
                    <div class="result-title">
                        <span class="difficulty">${'⭐'.repeat(problem.difficulty)}</span>
                        <span class="title">${this.highlightMatch(problem.title, query)}</span>
                    </div>
                    <div class="result-category">${problem.category}</div>
                </a>
            `).join('');

            this.searchResults.innerHTML = `
                <div class="results-header">
                    <span>${results.length} result${results.length !== 1 ? 's' : ''} found</span>
                    <button class="clear-search" onclick="problemSearch.clearSearch()">Clear</button>
                </div>
                <div class="results-list">
                    ${resultsHtml}
                </div>
            `;
        }

        this.searchResults.style.display = 'block';
    }

    highlightMatch(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    clearSearch() {
        this.searchInput.value = '';
        this.hideResults();
        this.searchInput.focus();
    }

    hideResults() {
        this.searchResults.style.display = 'none';
    }
}

// Initialize search when DOM is loaded
function initSearch() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.problemSearch = new ProblemSearch();
        });
    } else {
        window.problemSearch = new ProblemSearch();
    }
}

// Try to initialize immediately
initSearch();

// Also try after a short delay in case DOM is still loading
setTimeout(() => {
    if (!window.problemSearch) {
        console.log('Retrying search initialization...');
        window.problemSearch = new ProblemSearch();
    }
}, 1000);

// Main search functionality
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing main search...');
    
    const mainSearchInput = document.getElementById('main-search-input');
    const mainSearchResults = document.getElementById('main-search-results');
    const mainFilterBtns = document.querySelectorAll('.main-filter-btn');
    
    console.log('Search elements found:', {
        input: !!mainSearchInput,
        results: !!mainSearchResults,
        filterBtns: mainFilterBtns.length
    });
    
    if (mainSearchInput && mainSearchResults) {
        // Load all problems
        const allProblems = [];
        const problemLinks = document.querySelectorAll('a[href*="/problem_soulutions/"]');
        
        console.log('Found problem links:', problemLinks.length);
        
        problemLinks.forEach(link => {
            const title = link.textContent.trim();
            const url = link.href;
            
            if (title === 'Summary' || !url.includes('_analysis')) {
                return;
            }
            
            // Extract difficulty from title (stars)
            const difficultyMatch = title.match(/^(⭐+)\s/);
            const difficulty = difficultyMatch ? difficultyMatch[1].length : 0;
            const cleanTitle = title.replace(/^⭐+\s/, '');
            
            // Extract category from URL
            const categoryMatch = url.match(/problem_soulutions\/([^\/]+)/);
            const category = categoryMatch ? formatCategory(categoryMatch[1]) : '';
            
            allProblems.push({
                title: cleanTitle,
                fullTitle: title,
                url: url,
                difficulty: difficulty,
                category: category,
                searchText: `${cleanTitle} ${category} ${getDifficultyText(difficulty)}`.toLowerCase()
            });
        });
        
        console.log('Loaded problems for main search:', allProblems.length);
        
        // Filter button functionality
        mainFilterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                mainFilterBtns.forEach(b => {
                    b.style.background = 'white';
                    b.style.color = b.style.borderColor;
                });
                e.target.style.background = e.target.style.borderColor;
                e.target.style.color = 'white';
                performMainSearch();
            });
        });
        
        // Search input functionality
        mainSearchInput.addEventListener('input', performMainSearch);
        
        function performMainSearch() {
            console.log('Performing search...');
            const query = mainSearchInput.value.toLowerCase();
            const activeFilterBtn = document.querySelector('.main-filter-btn[style*="background"]');
            const activeFilter = activeFilterBtn ? activeFilterBtn.dataset.filter : 'all';
            console.log('Search query:', query, 'Active filter:', activeFilter);
            
            if (!query.trim()) {
                mainSearchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #6c757d;">Start typing to search problems...</div>';
                return;
            }
            
            const results = allProblems.filter(problem => {
                const matchesQuery = problem.searchText.includes(query);
                const matchesFilter = activeFilter === 'all' || problem.difficulty.toString() === activeFilter;
                return matchesQuery && matchesFilter;
            });
            
            console.log('Search results:', results.length, 'problems found');
            
            if (results.length === 0) {
                mainSearchResults.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: #6c757d;">
                        <p>🔍 No problems found for "${query}"</p>
                        <p>Try a different search term or check the filters</p>
                    </div>
                `;
            } else {
                const resultsHtml = results.map(problem => `
                    <a href="${problem.url}" style="display: block; padding: 15px; border-bottom: 1px solid #f1f3f4; text-decoration: none; color: inherit; transition: background 0.2s ease;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                            <span style="color: #ffc107; font-size: 14px; min-width: 30px;">${'⭐'.repeat(problem.difficulty)}</span>
                            <span style="font-weight: 500; font-size: 16px; color: #212529;">${highlightMatch(problem.title, query)}</span>
                        </div>
                        <div style="font-size: 14px; color: #6c757d; margin-left: 40px;">${problem.category}</div>
                    </a>
                `).join('');
                
                mainSearchResults.innerHTML = `
                    <div style="padding: 12px 15px; background: #f8f9fa; border-bottom: 1px solid #dee2e6; font-size: 14px; font-weight: 500; color: #495057;">
                        ${results.length} result${results.length !== 1 ? 's' : ''} found
                    </div>
                    ${resultsHtml}
                `;
            }
        }
        
        function formatCategory(category) {
            return category
                .split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        }
        
        function getDifficultyText(difficulty) {
            const difficulties = ['', 'Easy', 'Medium', 'Hard', 'Very Hard'];
            return difficulties[difficulty] || '';
        }
        
        function highlightMatch(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<mark style="background: #fff3cd; color: #856404; padding: 1px 2px; border-radius: 2px;">$1</mark>');
        }
        
        // Initialize with placeholder
        mainSearchResults.innerHTML = '<div style="padding: 20px; text-align: center; color: #6c757d;">Start typing to search problems...</div>';
    }
}); 
// Global state variable to track the active language
let currentLanguage = 'en'; 

// 1. FORCED REFRESH: Function called when EN, MR, KN, or TE buttons are clicked
async function switchLanguage(langCode) {
    // Standardize naming conventions
    if (langCode === 'kan') langCode = 'kn';
    if (langCode === 'telgu') langCode = 'te';
    
    currentLanguage = langCode;
    
    // Explicitly update the HTML document language attribute
    document.documentElement.lang = langCode;
    
    console.log(`Language switched to: ${langCode}. Fetching fresh translations...`);
    
    // Force a fresh download from Render using the new language parameter
    await loadPlotsData();
}

// 2. FULLY UPDATED: Fetch and immediately redraw cards on the screen
async function loadPlotsData() {
    try {
        console.log("Fetching plot advisory updates for language:", currentLanguage);

        // Fetch the fresh data layout passing the active language token (?lang=kn, ?lang=te, etc.)
        const response = await fetch(`${API_BASE_URL}/api/plots?lang=${currentLanguage}`);
        
        if (!response.ok) {
            throw new Error(`HTTP status: ${response.status}`);
        }
        
        const plots = await response.json();
        
        // Find the container element on your HTML page where the cards live
        // Note: Change 'plots-container' to match the actual ID used in your index.html!
        const container = document.getElementById('plots-container'); 
        
        if (container) {
            // WIPE OUT THE OLD CARDS completely so English doesn't stick around!
            container.innerHTML = ""; 
            
            // Re-render each plot card cleanly with the translated text
            plots.forEach(plot => {
                const card = document.createElement('div');
                card.className = 'plot-card';
                card.innerHTML = `
                    <h3>${plot.owner_name} — ${plot.crop === 'sugarcane' ? (currentLanguage === 'kn' ? 'ಕಬ್ಬು' : plot.crop) : plot.crop}</h3>
                    <p>📟 ಪ್ರದೇ: ${plot.acreage} ಎಕರೆಗಳು | 📅 ದಿನಾಂಕ: ${plot.date}</p>
                    <div class="advisory-box" style="white-space: pre-line; background: #fff8e7; padding: 15px; border-left: 4px solid #1b4d3e; margin-top: 10px;">
                        ${plot.advisory}
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
    } catch (error) {
        console.error("Error refreshing regional plots dashboard records:", error);
    }
}
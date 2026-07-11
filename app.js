// Base URL pointing to your live Render backend
const API_BASE_URL = "https://bos-app.onrender.com";

// Global state variable to track the active language (defaults to English)
let currentLanguage = 'en'; 

// Function to handle language selection switcher button updates
function switchLanguage(langCode) {
    // Standardize naming conventions if your UI passes 'kan' or 'telgu'
    if (langCode === 'kan') langCode = 'kn';
    if (langCode === 'telgu') langCode = 'te';
    
    currentLanguage = langCode;
    
    // Refresh the displayed data cards dynamically with the new language translation
    loadPlotsData();
}

// 1. Function to save plot data via FastAPI (POST Request)
async function saveUserData(farmerName, phoneNumber, crop) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/plots`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                farmer_name: farmerName,
                phone_number: phoneNumber,
                crop: crop,
                // Optional: You can pass the date selection value if pulled from your date form picker field
                date: new Date().toISOString().split('T')[0], 
                lang: currentLanguage
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Save Status:", data);
        
        // Refresh dashboard contents to show the newly added record instantly
        loadPlotsData();
        return data;
    } catch (error) {
        console.error("Error saving user data:", error);
        alert("Server error occurred while registering the plot.");
    }
}

// 2. UPDATED: Function to load plot layout cards dynamically using the selected language
async function loadPlotsData() {
    try {
        // Appends the current active language token parameter dynamically (?lang=kn, ?lang=te, etc.)
        const response = await fetch(`${API_BASE_URL}/api/plots?lang=${currentLanguage}`);
        
        if (!response.ok) {
            throw new Error(`HTTP status: ${response.status}`);
        }
        
        const plots = await response.json();
        console.log("Fetched Plots Data:", plots);
        
        // Call your existing frontend rendering UI function here to display plots on screen
        // Example: renderPlotsOnDashboard(plots);
        
    } catch (error) {
        console.error("Error fetching regional plots dashboard records:", error);
    }
}

// 3. NEW: Function to handle Admin Dashboard Verification Passwords
async function verifyAdminLogin(inputPassword) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: inputPassword })
        });
        
        const result = await response.json();
        
        if (result.status === "success") {
            alert("Access granted!");
            // Insert your frontend routing logic here to unlock dashboard views
            // Example: showAdminPanel();
        } else {
            alert("Access denied: " + result.message);
        }
    } catch (error) {
        console.error("Authentication server request failed:", error);
        alert("Error connecting to server verification service.");
    }
}
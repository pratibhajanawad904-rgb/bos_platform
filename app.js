// Change this to match your live codespace or temporary deployment domain
const API_BASE_URL = "https:bos-app.onrender.com"; // Auto-maps port if running locally side-by-side

// 1. Function to save user data to Firestore via FastAPI backend
async function saveUserData(userId, name, email) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/plots`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                name: name,
                email: email
            })
        });
        
        const data = await response.json();
        console.log("Save Status:", data);
        return data;
    } catch (error) {
        console.error("Error saving user data:", error);
    }
}

// 2. Function to fetch user data from Firestore via FastAPI backend
async function getUserData(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/get-user/${userId}`);
        const data = await response.json();
        console.log("Retrieved User Profile:", data);
        return data;
    } catch (error) {
        console.error("Error fetching user data:", error);
    }
}
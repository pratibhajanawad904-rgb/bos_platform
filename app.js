// Base URL pointing to your live Render backend
const API_BASE_URL = "https://bos-app.onrender.com";

// 1. Function to save plot data to Firestore via FastAPI
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
                crop: crop
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Save Status:", data);
        return data;
    } catch (error) {
        console.error("Error saving user data:", error);
        alert("Server error occurred while registering the plot.");
    }
}

// 2. Setup Form Submission Event Listener
document.addEventListener("DOMContentLoaded", () => {
    // Select your form element (adjust selector if your form has a different ID/class)
    const registerForm = document.querySelector("form") || document.getElementById("registerForm");
    
    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault(); // Stop page from reloading

            // Get inputs from the UI fields
            const farmerNameInput = document.getElementById("farmerName") || document.querySelector("input[placeholder='pratibha']");
            const mobileNumberInput = document.getElementById("mobileNumber") || document.querySelector("input[placeholder='8618734070']");
            const selectCropElement = document.getElementById("selectCrop") || document.querySelector("select");

            const farmerName = farmerNameInput ? farmerNameInput.value.trim() : "";
            const phoneNumber = mobileNumberInput ? mobileNumberInput.value.trim() : "";
            const crop = selectCropElement ? selectCropElement.value : "";

            if (!farmerName || !phoneNumber || !crop) {
                alert("Please fill in all required fields.");
                return;
            }

            console.log("Submitting:", { farmerName, phoneNumber, crop });
            
            // Call the API function
            const result = await saveUserData(farmerName, phoneNumber, crop);
            
            if (result) {
                alert("Layout successfully registered!");
                registerForm.reset(); // Clear form fields
            }
        });
    }
});
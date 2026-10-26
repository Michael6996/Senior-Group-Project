//below code will get internships from the Flask backend
async function loadInternships() {
    try {
        const response = await fetch("/api/internships");

        if (!response.ok) {
            throw new Error("Failed to load internships");
        }

        const internships = await response.json();

        // for now, display the internships in the browser console
        console.log("Internships from database:", internships);

    } catch (error) {
        console.error("Error loading internships:", error);
    }
}

// run when the webpage finishes loading
document.addEventListener("DOMContentLoaded", loadInternships);
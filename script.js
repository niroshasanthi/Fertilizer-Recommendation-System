document.getElementById("predictForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent page reload

    let data = {
        temperature: parseFloat(document.getElementById("temperature").value),
        humidity: parseFloat(document.getElementById("humidity").value),
        moisture: parseFloat(document.getElementById("moisture").value),
        soil_type: document.getElementById("soil_type").value.toLowerCase(),
        crop_type: document.getElementById("crop_type").value.toLowerCase(),
        nitrogen: parseFloat(document.getElementById("nitrogen").value),
        phosphorus: parseFloat(document.getElementById("phosphorus").value),
        potassium: parseFloat(document.getElementById("potassium").value)
    };

    console.log("Sending data:", data); // Debugging 🚀

    try {
        let response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        let result = await response.json();
        console.log("Server response:", result); // Debugging 🚀

        if (response.ok) {
            document.getElementById("result").innerText = "Recommended Fertilizer: " + result.recommended_fertilizer;
        } else {
            document.getElementById("result").innerText = "Error: " + (result.error || "Unknown error occurred");
        }
    } catch (error) {
        console.error("Error fetching prediction:", error);
        document.getElementById("result").innerText = "Server Error! Unable to connect.";
    }
});

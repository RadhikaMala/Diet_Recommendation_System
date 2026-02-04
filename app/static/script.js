function getDiet() {
    console.log("Button clicked");  // 🔍 DEBUG

    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const exercise = document.getElementById("exercise").value;
    const sleep = document.getElementById("sleep").value;

    if (!age || !height || !weight || !exercise || !sleep) {
        alert("Please fill all fields");
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            age, gender, height, weight, exercise, sleep
        })
    })
    .then(res => res.json())
    .then(result => {

        const dietImages = {
            "Balanced Diet": "balanced.jpg",
            "Low Fat Diet": "low_fat.jpg",
            "High Protein Diet": "high_protein.jpg",
            "Vegan Diet": "vegan.jpg",
            "Keto Diet": "keto.jpg",
            "Mediterranean Diet": "mediterranean.jpg"
        };

        const img = dietImages[result.diet] || "balanced.jpg";

        const resultDiv = document.getElementById("result");
        resultDiv.classList.remove("hidden");

        resultDiv.innerHTML = `
            <h3>✅ Recommendation</h3>
            <p><strong>BMI:</strong> ${result.bmi} (${result.bmi_category})</p>
            <p><strong>Meal Plan:</strong> ${result.diet}</p>
            <img src="/static/images/${img}" class="diet-image">
        `;
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Something went wrong. Check console.");
    });
}

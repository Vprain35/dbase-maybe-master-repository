// DOM elements
const yearDropdown = document.getElementById("year-dropdown");
const teamsList = document.getElementById("teams-list");

// Fetch years from backend
async function loadYears() {
    try {
        const response = await fetch("/years");
        if (!response.ok) throw new Error("Failed to fetch years");
        const years = await response.json();

        // Clear current options
        yearDropdown.innerHTML = "";

        // Default option
        const defaultOption = document.createElement("option");
        defaultOption.textContent = "Select a year...";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        yearDropdown.appendChild(defaultOption);

        // Add year options
        years.forEach(year => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = year;
            yearDropdown.appendChild(option);
        });
    } catch (error) {
        yearDropdown.innerHTML = `<option>Error loading years</option>`;
        console.error(error);
    }
}

// Fetch teams for selected year
async function loadTeams(year) {
    try {
        const response = await fetch(`/teams?year=${year}`);
        if (!response.ok) throw new Error("No teams found for this year");
        const teams = await response.json();

        // Clear previous list
        teamsList.innerHTML = "";

        // Populate list
        teams.forEach(teamName => {
            const div = document.createElement("div");
            div.className = "team-item";
            div.textContent = teamName;
            teamsList.appendChild(div);
        });
    } catch (error) {
        teamsList.innerHTML = `<div class="team-item">No teams found for year ${year}</div>`;
        console.error(error);
    }
}

// Event listener for year selection
yearDropdown.addEventListener("change", (event) => {
    const year = event.target.value;
    loadTeams(year);
});

// Load years on page load
document.addEventListener("DOMContentLoaded", loadYears);
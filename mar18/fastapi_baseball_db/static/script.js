// DOM elements
const yearDropdown = document.getElementById("year-dropdown");
const teamsList = document.getElementById("teams-list");
const playersList = document.getElementById("players-list");
const playerInfo = document.getElementById("player-info");

// Load years from backend
async function loadYears() {
    try {
        const response = await fetch("/years");
        if (!response.ok) throw new Error("Failed to fetch years");
        const years = await response.json();

        yearDropdown.innerHTML = "";
        const defaultOption = document.createElement("option");
        defaultOption.textContent = "Select a year...";
        defaultOption.disabled = true;
        defaultOption.selected = true;
        yearDropdown.appendChild(defaultOption);

        years.forEach(year => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = year;
            yearDropdown.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        yearDropdown.innerHTML = `<option>Error loading years</option>`;
    }
}

// Load teams for selected year
async function loadTeams(year) {
    try {
        const response = await fetch(`/teams?year=${year}`);
        if (!response.ok) throw new Error("No teams found for this year");
        const teams = await response.json();

        teamsList.innerHTML = "";
        playersList.innerHTML = "";
        playerInfo.innerHTML = "";

        // Group teams by league/division
        const grouped = {};
        teams.forEach(team => {
            const key = `${team.lgID}-${team.divID}`;
            if (!grouped[key]) grouped[key] = [];
            grouped[key].push(team);
        });

        // Display teams
        for (const key in grouped) {
            const [lg, div] = key.split("-");
            const header = document.createElement("h3");
            header.textContent = `${lg} - ${div}`;
            teamsList.appendChild(header);

            grouped[key].forEach(team => {
                const divEl = document.createElement("div");
                divEl.className = "team-item";
                divEl.textContent = team.name;
                divEl.dataset.teamId = team.teamID;
                divEl.addEventListener("click", () => loadPlayers(year, team.teamID));
                teamsList.appendChild(divEl);
            });
        }
    } catch (error) {
        console.error(error);
        teamsList.innerHTML = `<div class="team-item">No teams found</div>`;
    }
}

// Load players for a team
async function loadPlayers(year, teamID) {
    try {
        const response = await fetch(`/players?year=${year}&teamID=${teamID}`);
        if (!response.ok) throw new Error("No players found for this team");
        const players = await response.json();

        playersList.innerHTML = "";
        playerInfo.innerHTML = "";

        players.forEach(player => {
            const divEl = document.createElement("div");
            divEl.className = "team-item";
            divEl.textContent = player.name;
            divEl.dataset.playerId = player.playerID;
            divEl.addEventListener("click", () => loadPlayerInfo(player.playerID));
            playersList.appendChild(divEl);
        });
    } catch (error) {
        console.error(error);
        playersList.innerHTML = `<div class="team-item">No players found</div>`;
    }
}

// Load full player info and display nicely
async function loadPlayerInfo(playerID) {
    try {
        const response = await fetch(`/player-info-full?playerID=${playerID}`);
        if (!response.ok) throw new Error("Player info not found");
        const data = await response.json();

        const playerInfo = document.getElementById("player-info");
        playerInfo.innerHTML = "";

        // Personal info card
        const personal = data.personal || {};
        const personalCard = document.createElement("div");
        personalCard.className = "info-card";

        personalCard.innerHTML = `
            <h3>${personal.nameFirst || ""} ${personal.nameLast || ""}</h3>
            <p><strong>Given Name:</strong> ${personal.nameGiven || "N/A"}</p>
            <p><strong>Birth:</strong> ${personal.birthYear || "?"}-${personal.birthMonth || "?"}-${personal.birthDay || "?"} in ${personal.birthCity || ""}, ${personal.birthState || ""}, ${personal.birthCountry || ""}</p>
            <p><strong>Death:</strong> ${personal.deathYear || "?"}-${personal.deathMonth || "?"}-${personal.deathDay || "?"} in ${personal.deathCity || ""}, ${personal.deathState || ""}, ${personal.deathCountry || ""}</p>
            <p><strong>Height / Weight:</strong> ${personal.height || "?"} / ${personal.weight || "?"}</p>
            <p><strong>Bats / Throws:</strong> ${personal.bats || "?"} / ${personal.throws || "?"}</p>
            <p><strong>Debut:</strong> ${personal.debut || "N/A"}</p>
            <p><strong>Final Game:</strong> ${personal.finalGame || "N/A"}</p>
            <p><strong>BBRef ID:</strong> ${personal.bbrefID || "N/A"} | <strong>Retro ID:</strong> ${personal.retroID || "N/A"}</p>
        `;
        playerInfo.appendChild(personalCard);

        // Batting info card
        const battingCard = document.createElement("div");
        battingCard.className = "info-card";

        if (data.battingStats && data.battingStats.length > 0) {
            const table = document.createElement("table");

            // table header
            const headerRow = document.createElement("tr");
            Object.keys(data.battingStats[0]).forEach(key => {
                const th = document.createElement("th");
                th.textContent = key;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);

            // table rows
            data.battingStats.forEach(row => {
                const tr = document.createElement("tr");
                Object.values(row).forEach(val => {
                    const td = document.createElement("td");
                    td.textContent = val ?? "-";
                    tr.appendChild(td);
                });
                table.appendChild(tr);
            });

            battingCard.appendChild(table);
        } else {
            battingCard.innerHTML = "<p>No batting stats found</p>";
        }

        playerInfo.appendChild(battingCard);

    } catch (error) {
        console.error(error);
        document.getElementById("player-info").innerHTML = `<div class="team-item">No player info found</div>`;
    }
}

// Event listener
yearDropdown.addEventListener("change", (event) => loadTeams(event.target.value));

// Initialize
document.addEventListener("DOMContentLoaded", loadYears);
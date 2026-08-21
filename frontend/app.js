const API_URL = "/api";

async function loadCandidates() {
    try {
        const response = await fetch(`${API_URL}/candidates/`);

        if (!response.ok) {
            throw new Error("Failed to load candidates");
        }

        const candidates = await response.json();

        displayCandidates(candidates);
        populateCandidateSelects(candidates);

    } catch (error) {
        showMessage(
            "candidate-message",
            error.message,
            true
        );
    }
}

function displayCandidates(candidates) {
    const tableBody =
        document.getElementById("candidate-table-body");

    tableBody.innerHTML = "";

    candidates.forEach(candidate => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${candidate.full_name}</td>
            <td>${candidate.email}</td>
            <td>${candidate.training_track}</td>
            <td>${candidate.is_active ? "Yes" : "No"}</td>

            <td>
                <button onclick="editCandidate(${candidate.id})">
                    Edit
                </button>

                <button onclick="deleteCandidate(${candidate.id})">
                    Delete
                </button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}


function populateCandidateSelects(candidates) {

    const statusSelect =
        document.getElementById("status-candidate");

    const filterSelect =
        document.getElementById("status-candidate-filter");

    statusSelect.innerHTML =
        '<option value="">Select Candidate</option>';

    filterSelect.innerHTML =
        '<option value="">All Candidates</option>';

    candidates.forEach(candidate => {

        const statusOption =
            document.createElement("option");

        statusOption.value = candidate.id;
        statusOption.textContent =
            candidate.full_name;

        statusSelect.appendChild(statusOption);


        const filterOption =
            document.createElement("option");

        filterOption.value = candidate.id;
        filterOption.textContent =
            candidate.full_name;

        filterSelect.appendChild(filterOption);
    });
}


document
    .getElementById("candidate-form")
    .addEventListener("submit", async function(event) {
        event.preventDefault();

        const candidateData = {
            full_name: document.getElementById("candidate-name").value,
            email: document.getElementById("candidate-email").value,
            training_track: document.getElementById("training-track").value,
            is_active: document.getElementById("candidate-active").checked
        };

        try {
            const response = await fetch(`${API_URL}/candidates/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(candidateData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Request failed");
            }

            showMessage("candidate-message", "Candidate saved successfully.");
            resetCandidateForm();

            await loadCandidates();
            await loadDashboard();

        } catch (error) {
            showMessage("candidate-message", error.message, true);
        }
    });


// 1. Open Candidate Modal and Populate Fields
async function editCandidate(candidateId) {
    const modalMsg = document.getElementById("modal-candidate-message");
    if (modalMsg) {
        modalMsg.innerHTML = "";
        modalMsg.className = "message";
    }

    try {
        const response = await fetch(`${API_URL}/candidates/${candidateId}`);

        if (!response.ok) {
            throw new Error("Candidate not found");
        }

        const candidate = await response.json();

        document.getElementById("edit-candidate-id").value = candidate.id;
        document.getElementById("edit-candidate-name").value = candidate.full_name;
        document.getElementById("edit-candidate-email").value = candidate.email;
        document.getElementById("edit-training-track").value = candidate.training_track;
        document.getElementById("edit-candidate-active").checked = candidate.is_active;

        document.getElementById("candidate-edit-modal").classList.add("active");

    } catch (error) {
        showMessage("candidate-message", error.message, true);
    }
}

// 2. Close Candidate Modal
function closeCandidateEditModal() {
    document.getElementById("candidate-edit-modal").classList.remove("active");
    document.getElementById("candidate-edit-form").reset();
}

// 3. Candidate Modal Submit Listener
document
    .getElementById("candidate-edit-form")
    .addEventListener("submit", async function(event) {
        event.preventDefault();

        const candidateId = document.getElementById("edit-candidate-id").value;

        const candidateData = {
            full_name: document.getElementById("edit-candidate-name").value,
            email: document.getElementById("edit-candidate-email").value,
            training_track: document.getElementById("edit-training-track").value,
            is_active: document.getElementById("edit-candidate-active").checked
        };

        try {
            const response = await fetch(`${API_URL}/candidates/${candidateId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(candidateData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Update failed");
            }

            closeCandidateEditModal();
            showMessage("candidate-message", "Candidate updated successfully.");

            await loadCandidates();
            await loadDashboard();

        } catch (error) {
            showMessage("modal-candidate-message", error.message, true);
        }
    });

async function deleteCandidate(candidateId) {

    const confirmed = confirm(
        "Are you sure you want to delete this candidate?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/candidates/${candidateId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Delete failed");
        }

        showMessage(
            "candidate-message",
            "Candidate deleted successfully."
        );

        await loadCandidates();
        await loadDashboard();

    } catch (error) {

        showMessage(
            "candidate-message",
            error.message,
            true
        );
    }
}


function resetCandidateForm() {

    document
        .getElementById("candidate-form")
        .reset();

    document.getElementById("candidate-id").value = "";

    document.getElementById("candidate-active").checked = true;
}


document
    .getElementById("cancel-edit")
    .addEventListener("click", resetCandidateForm);


document
    .getElementById("status-form")
    .addEventListener("submit", async function(event) {
        event.preventDefault();

        // CLEANUP: Removed the 'statusId' check entirely since this is POST-only now
        const statusData = {
            candidate_id: Number(document.getElementById("status-candidate").value),
            status_date: document.getElementById("status-date").value,
            work_completed: document.getElementById("work-completed").value,
            topics_learned: document.getElementById("topics-learned").value,
            blockers: document.getElementById("blockers").value,
            next_day_plan: document.getElementById("next-day-plan").value,
            completion_percentage: Number(document.getElementById("completion-percentage").value)
        };

        try {
            const response = await fetch(`${API_URL}/statuses/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(statusData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Failed to submit status");
            }

            showMessage("status-message", "Daily status submitted successfully.");

            // Reset the creation form fields cleanly
            document.getElementById("status-form").reset();

            // Refresh layout numbers and history data logs
            await loadDashboard();
            await loadStatusHistory();

        } catch (error) {
            showMessage("status-message", error.message, true);
        }
    });



async function loadStatusHistory() {

    // 1. Get the element once
    const messageElement = document.getElementById("status-history-message");
    
    // 2. Clear the text AND hide the container entirely
    messageElement.innerHTML = "";
    messageElement.style.display = "none"; 

    try {

        const candidateId =
            document.getElementById(
                "status-candidate-filter"
            ).value;

        const statusDate =
            document.getElementById(
                "status-date-filter"
            ).value;

        const dateFrom =
            document.getElementById(
                "status-date-from"
            ).value;

        const dateTo =
            document.getElementById(
                "status-date-to"
            ).value;


        const params = new URLSearchParams();

        if (dateFrom && dateTo && dateFrom > dateTo) {

            throw new Error(
                "The 'From' date cannot be later than the 'To' date."
            );
        }

        if (
            statusDate &&
            (dateFrom || dateTo)
        ) {
            throw new Error(
                "Use either a specific date or a date range, not both."
            );
        }

        if (candidateId) {
            params.append(
                "candidate_id",
                candidateId
            );
        }

        if (statusDate) {
            params.append(
                "status_date",
                statusDate
            );
        }

        if (dateFrom) {
            params.append(
                "date_from",
                dateFrom
            );
        }

        if (dateTo) {
            params.append(
                "date_to",
                dateTo
            );
        }


        const response = await fetch(
            `${API_URL}/statuses/?${params.toString()}`
        );

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.detail ||
                "Failed to load status history"
            );
        }


        const statuses = await response.json();

        displayStatusHistory(statuses);

    } catch (error) {
        messageElement.style.display = "block";
        showMessage(
            "status-history-message",
            error.message,
            true
        );
    }
}


function displayStatusHistory(statuses) {
    const tableBody = document.getElementById("status-history-table-body");
    tableBody.innerHTML = "";

    statuses.forEach(status => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td><strong style="color: var(--text-primary);">${status.candidate_name || 'N/A'}</strong></td>
            <td><span class="badge-tech">${status.status_date}</span></td>
            <td>${status.work_completed}</td>
            <td>${status.topics_learned}</td>
            <td>${status.blockers ? `<span style="color: var(--color-error);">${status.blockers}</span>` : '<span style="color: var(--text-muted);">None</span>'}</td>
            <td>${status.next_day_plan || 'N/A'}</td>
            <td><strong>${status.completion_percentage}%</strong></td>
            <td>
                <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px; margin-right: 4px;" onclick="editStatus(${status.id})">
                    Edit
                </button>
                <button class="btn-secondary" style="padding: 4px 10px; font-size: 12px; color: var(--color-error); border-color: rgba(239,68,68,0.2);" onclick="deleteStatus(${status.id})">
                    Delete
                </button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}



// 1. Open Modal and Populate Fields
async function editStatus(statusId) {
    const modalMsg = document.getElementById("modal-status-message");
    if (modalMsg) {
        modalMsg.innerHTML = "";
        modalMsg.className = "message";
    }

    try {
        const response = await fetch(`${API_URL}/statuses/${statusId}`);

        if (!response.ok) {
            throw new Error("Status record not found on server.");
        }

        const status = await response.json();

        // Dynamically copy candidate select options from original form to modal form
        const originalSelect = document.getElementById("status-candidate");
        const modalSelect = document.getElementById("edit-status-candidate");
        if (originalSelect && modalSelect) {
            modalSelect.innerHTML = originalSelect.innerHTML;
        }

        // Fill out modal inputs
        document.getElementById("edit-status-id").value = status.id;
        document.getElementById("edit-status-candidate").value = status.candidate_id;
        document.getElementById("edit-status-date").value = status.status_date;
        document.getElementById("edit-work-completed").value = status.work_completed;
        document.getElementById("edit-topics-learned").value = status.topics_learned;
        document.getElementById("edit-blockers").value = status.blockers || "";
        document.getElementById("edit-next-day-plan").value = status.next_day_plan || "";
        document.getElementById("edit-completion-percentage").value = status.completion_percentage;

        // Open Modal visually
        document.getElementById("status-edit-modal").classList.add("active");

    } catch (error) {
        showMessage("status-history-message", error.message, true);
    }
}

// 2. Close Modal
function closeEditModal() {
    document.getElementById("status-edit-modal").classList.remove("active");
    document.getElementById("status-edit-form").reset();
}

// 3. Separate Modal Form Submit Event Listener
document
    .getElementById("status-edit-form")
    .addEventListener("submit", async function(event) {
        event.preventDefault();

        const statusId = document.getElementById("edit-status-id").value;

        const updatedData = {
            candidate_id: Number(document.getElementById("edit-status-candidate").value),
            status_date: document.getElementById("edit-status-date").value,
            work_completed: document.getElementById("edit-work-completed").value,
            topics_learned: document.getElementById("edit-topics-learned").value,
            blockers: document.getElementById("edit-blockers").value,
            next_day_plan: document.getElementById("edit-next-day-plan").value,
            completion_percentage: Number(document.getElementById("edit-completion-percentage").value)
        };

        try {
            const response = await fetch(`${API_URL}/statuses/${statusId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatedData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || "Failed to update status record.");
            }

            // Close window and refresh main view dashboard layouts
            closeEditModal();
            showMessage("status-history-message", "Daily status updated successfully.");
            
            await loadDashboard();
            await loadStatusHistory();

        } catch (error) {
            showMessage("modal-status-message", error.message, true);
        }
    });


async function deleteStatus(statusId) {
    const confirmed = confirm("Are you sure you want to delete this status entry?");
    if (!confirmed) return;

    try {
        const response = await fetch(`${API_URL}/statuses/${statusId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Delete failed");
        }

        showMessage("status-history-message", "Status deleted successfully.");
        
        // Refresh the dashboard and table numbers
        await loadStatusHistory();
        await loadDashboard();

    } catch (error) {
        showMessage("status-history-message", error.message, true);
    }
}



async function loadDashboard() {

    try {

        const selectedDate =
            document.getElementById("dashboard-date").value;

        if (!selectedDate) {
            throw new Error("Please select a date.");
        }

        const response = await fetch(
            `${API_URL}/dashboard/summary?date=${selectedDate}`
        );

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.detail || "Failed to load dashboard"
            );
        }

        const dashboard = await response.json();


        // -----------------------------
        // Summary cards
        // -----------------------------

        document.getElementById("total-active").textContent =
            dashboard.total_active_candidates;

        document.getElementById("submitted-today").textContent =
            dashboard.submitted_count;

        document.getElementById("missing-today").textContent =
            dashboard.missing_count;

        document.getElementById("average-completion").textContent =
            `${dashboard.average_completion_percentage}%`;


        // -----------------------------
        // Missing candidates
        // -----------------------------

        const missingList =
            document.getElementById("missing-candidates");

        missingList.innerHTML = "";

        if (dashboard.missing_candidates.length === 0) {

            const item =
                document.createElement("li");

            item.textContent =
                "All active candidates submitted their status.";

            missingList.appendChild(item);

        } else {

            dashboard.missing_candidates.forEach(
                candidate => {

                    const item =
                        document.createElement("li");

                    item.textContent =
                        `${candidate.candidate_name} (${candidate.email})`;

                    missingList.appendChild(item);
                }
            );
        }


        // -----------------------------
        // Latest statuses
        // -----------------------------

        const latestTable =
            document.getElementById(
                "latest-status-table-body"
            );

        latestTable.innerHTML = "";

        if (dashboard.latest_statuses.length === 0) {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td colspan="3">
                    No statuses have been submitted yet.
                </td>
            `;

            latestTable.appendChild(row);

        } else {

            dashboard.latest_statuses.forEach(
                status => {

                    const row =
                        document.createElement("tr");

                    row.innerHTML = `
                        <td>${status.candidate_name}</td>
                        <td>${status.status_date}</td>
                        <td>${status.completion_percentage}%</td>
                    `;

                    latestTable.appendChild(row);
                }
            );
        }

    } catch (error) {

        showMessage(
            "dashboard-message",
            error.message,
            true
        );
    }
}

function setDashboardDate() {

    const dateInput =
        document.getElementById("dashboard-date");

    const today =
        new Date().toISOString().split("T")[0];

    dateInput.value = today;
}

document
    .getElementById("dashboard-load")
    .addEventListener(
        "click",
        loadDashboard
    );

        document
            .getElementById("status-filter-button")
            .addEventListener(
                "click",
                loadStatusHistory
            );


        document
            .getElementById("status-clear-filter-button")
            .addEventListener(
                "click",
                clearStatusFilters
            );

function showMessage(elementId, message, isError = false) {

    const element =
        document.getElementById(elementId);

    element.textContent = message;

    element.className =
        isError ? "message error" : "message success";
}


function setStatusDateLimit() {

    const dateInput =
        document.getElementById("status-date");

    const today =
        new Date().toISOString().split("T")[0];

    dateInput.max = today;
}

document.addEventListener(
    "DOMContentLoaded",
    function() {

        setDashboardDate();

        loadCandidates();

        loadDashboard();

        loadStatusHistory();

        setStatusDateLimit();

    }
);

function clearStatusFilters() {

    document.getElementById(
        "status-candidate-filter"
    ).value = "";

    document.getElementById(
        "status-date-filter"
    ).value = "";

    document.getElementById(
        "status-date-from"
    ).value = "";

    document.getElementById(
        "status-date-to"
    ).value = "";

    loadStatusHistory();
}

// Close modal if the user clicks anywhere on the dark background overlay
window.addEventListener("click", function(event) {
    const modal = document.getElementById("status-edit-modal");
    if (event.target === modal) {
        closeEditModal();
    }
});

window.addEventListener("click", function(event) {
    const statusModal = document.getElementById("status-edit-modal");
    const candidateModal = document.getElementById("candidate-edit-modal");

    if (event.target === statusModal) {
        closeEditModal();
    }
    if (event.target === candidateModal) {
        closeCandidateEditModal();
    }
});
document.getElementById("update-progress").addEventListener("click", function() {
    let coding = prompt("Enter coding questions completed this week:");
    let badges = prompt("Enter number of badges earned:");
    let aptitude = prompt("Enter aptitude topics covered:");

    if (coding) document.getElementById("coding-count").textContent = coding;
    if (badges) document.getElementById("badge-count").textContent = badges;
    if (aptitude) document.getElementById("aptitude-count").textContent = aptitude;

    // Save progress in LocalStorage
    localStorage.setItem("codingCount", coding);
    localStorage.setItem("badgeCount", badges);
    localStorage.setItem("aptitudeCount", aptitude);
});

// Load stored progress
window.onload = function() {
    document.getElementById("coding-count").textContent = localStorage.getItem("codingCount") || 0;
    document.getElementById("badge-count").textContent = localStorage.getItem("badgeCount") || 0;
    document.getElementById("aptitude-count").textContent = localStorage.getItem("aptitudeCount") || 0;
};

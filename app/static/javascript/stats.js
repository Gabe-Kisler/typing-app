


let userStats = {};
const statsMap = {
    "total-tests": "total_tests",
    "time-typing-num": "typing_time",
    "best-wpm-num": "best_ovr_wpm",
    "fifteen-best": "fifteen_sec_best",
    "fifteen-avg": "fifteen_sec_avg",
    "fifteen-tests": "fifteen_sec_tests",
    "thirty-best": "thirty_sec_best",
    "thirty-avg": "thirty_sec_avg",
    "thirty-tests": "thirty_sec_tests",
    "sixty-best": "sixty_sec_best",
    "sixty-avg": "sixty_sec_avg",
    "sixty-tests": "sixty_sec_tests"
};

window.onload = function() {
    fetch ('/retrieve-stats', { method: 'POST' })
        .then (response => response.json())
        .then (data => {
            console.log ('stats retrieved', data);
            userStats = data;
            displayStats();
        })
        .catch (error => console.log('could not retrieve stats', error));
}

function getStatsElement(elementName) {
    return document.getElementById (elementName);
}

function displayStats () {
    for (const [elementId, jsonKey] of Object.entries(statsMap)) {
        let statVal = userStats[jsonKey];
        let element = getStatsElement(elementId);
        if (element) {
            element.textContent = statVal;
        }
    }
}

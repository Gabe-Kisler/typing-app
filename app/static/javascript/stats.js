window.onload = function() {
    fetch ('/retrieve-stats', { method: 'POST' })
        .then (response => response.json())
        .then (data => {
            console.log ('stats retrieved', data);
            userStats = data;
        })
        .catch (error => console.log('could not retrieve stats', error));
}

function parseStats () {

}
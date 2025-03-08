const signupScreenButton = document.getElementById('signupScreen');
const loginScreenButton = document.getElementById('loginScreen');
const signupButton = document.getElementById('signupButton');
const loginDiv = document.getElementById('login');
const signupDiv = document.getElementById('createAccount');

window.onload = function() {
    clickListeners();
}

function clickListeners() {
    [signupScreenButton, loginScreenButton, signupButton].forEach( button => {
        button.addEventListener('click', (event) => {
            initializeButtonFunctions (event.target.id);
        });
    });
}

function initializeButtonFunctions(buttonPressed) {
    if (buttonPressed === "signupScreen") {
        toggleDisplays('signup');
    }
    else if (buttonPressed === "loginScreen") { 
        toggleDisplays('login');
    }
    else if (buttonPressed === "signupButton") {
        signupUser();
    }
}

function toggleDisplays(screen) {
    if (screen === 'signup') {
        loginDiv.style.display = 'none';
        signupDiv.style.display = 'block';
    }
    else {
        loginDiv.style.display = 'block';
        signupDiv.style.display = 'none';
    }

    clickListeners();

}

function signupUser(event) {
    event.preventDefault();

    const username = document.getElementById('createUsername').value;
    const password = document.getElementById('createPassword').value;
    const email = document.getElementById('createEmail').value;
    const user = {username, password, email};


    fetch ('/create-account', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })

    .then(response => { 
        if (response.ok) {
            return response.json();
        }
        else {
            throw new Error ('could not create account');
        }
    })
    .then (result => {
        console.log ('Account created:', result);
        window.location.assign('/login');
    })
    .catch(error => {
        console.error ('error:', error);
    })
}



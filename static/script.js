document.getElementById('signupScreen').addEventListener('click', function(){
    document.getElementById('login').style.display = 'none';
    document.getElementById('createAccount').style.display = 'block';
});

document.getElementById('loginScreen').addEventListener('click', function(){
    document.getElementById('login').style.display = 'block';
    document.getElementById('createAccount').style.display = 'none';
});

document.getElementById('signupButton').addEventListener('click', function(e){
    e.preventDefault();
    const username = document.getElementById('createUsername').value;
    const password = document.getElementById('createPassword').value;
    const email = document.getElementById('createEmail').value;

    const user = {
        username: username,
        password: password,
        email: email
    };

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



});



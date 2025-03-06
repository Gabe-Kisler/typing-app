const easy = document.getElementById('Easy');
const medium = document.getElementById('Medium');
const hard = document.getElementById('Hard');
const fifteen = document.getElementById('fifteen');
const thirty = document.getElementById('thirty');
const sixty = document.getElementById('sixty');

let count = 0;
let currentWords = null;
let defaultMode = 'easy';

function loadWords (buttonChoice) {
    fetch ('/get-words', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({level: buttonChoice})
    })
    .then (response => response.json())
    .then (data => {
        currentWords = data.wordsString;
        console.log ("words:", data);
        const displayText = document.getElementById('display-text');
        displayText.textContent = data.wordsString;
    })
    .catch (error => {
        console.error ('error getting words', error);
    });
}


let timeChoice = '15';

window.onload = function() {
    loadWords("easy");
    easy.addEventListener('click', function() {
        defaultMode = 'easy';
        loadWords("easy");
    })
    medium.addEventListener('click', function() {
        defaultMode = 'medium';
        loadWords("medium");
    })    
    hard.addEventListener('click', function() {
        defaultMode = 'hard';
        loadWords("hard");
    })
    fifteen.addEventListener('click', function() {
        timeChoice = '15';
        loadWords (defaultMode);
    })
    thirty.addEventListener('click', function() {
        timeChoice = '30';
        loadWords (defaultMode);
    })
    sixty.addEventListener('click', function() {
        timeChoice = '60'
        loadWords (defaultMode);
    })
    toggleDefaults();
    setTimer(15);
} 


function toggleButtonColor (button) {
    button.addEventListener('click', function() {
        if (button == easy || button == hard || button == medium) {
            easy.classList.remove('active');
            medium.classList.remove('active');
            hard.classList.remove('active');
        }

        else if (button == fifteen) {
            fifteen.classList.remove('active');
            thirty.classList.remove('active');
            sixty.classList.remove('active');

            setTimer (15);

        } 
        else if (button === thirty) {
            fifteen.classList.remove('active');
            thirty.classList.remove('active');
            sixty.classList.remove('active');

            setTimer(30);
        } 
        else if (button === sixty) {
            fifteen.classList.remove('active');
            thirty.classList.remove('active');
            sixty.classList.remove('active');

            setTimer(60);

        }

        

        button.classList.toggle('active');
    });
}

    function toggleDefaults () {
        fifteen.classList.toggle('active');
        easy.classList.toggle('active');
    }

    toggleButtonColor(easy);
    toggleButtonColor(medium);
    toggleButtonColor(hard);
    toggleButtonColor(fifteen);
    toggleButtonColor(thirty);
    toggleButtonColor(sixty);


    let timerInterval = null;

    function startTimer (time) {
        if (timerInterval !== null) {
            clearInterval(timerInterval);
        }
        const timer = document.getElementById('timer');
        let count = time;
        timer.textContent = count;

        timerInterval = setInterval (function() {
            count--;
            timer.textContent = count;
    
    
            if (count <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        }, 1000)
    }

    function setTimer (time) {
        const timer = document.getElementById('timer');
        let timerTime = time;
        timer.textContent = timerTime;
    }

    let testString = [];

    document.addEventListener ('keyup', function(event) {
        if (event.key === 'Enter') {
            count = 0;
            refreshTestString();
            getTextField();
            if (timeChoice === '15') {
                startTimer(15);
            }
            else if (timeChoice === '30') {
                startTimer(30);
            }
            else if (timeChoice ==='60') {
                startTimer(60);
            }
            return;
        }

        const characterArray = currentWords.split("");

        if (event.key === characterArray[count]) {
            changeCharacterColor (count, 'green');
        }
        else {
            changeCharacterColor (count, 'red');
        }
        count ++ 
        getTextField();
    });

    function refreshTestString () {
        testString = currentWords.split("").map(char => `<span>${char}</span>`);
    }


    function changeCharacterColor (index, color) {
        const char = currentWords [index];
        testString [index] = `<span style="color:${color};">${char}</span>`;
    }

    function getTextField () {
        const textField = document.getElementById('display-text');
        textField.innerHTML = testString.join("");
    }

    


 
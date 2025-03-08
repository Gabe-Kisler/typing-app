const easy = document.getElementById('Easy');
const medium = document.getElementById('Medium');
const hard = document.getElementById('Hard');
const fifteen = document.getElementById('fifteen');
const thirty = document.getElementById('thirty');
const sixty = document.getElementById('sixty');

const LEVELS = {
    easy: 'easy',
    medium: 'medium',
    hard: 'hard'
};

const TIME_OPTIONS = {
    fifteen: '15',
    thirty: '30', 
    sixty: '60'
};

const COLORS = {
    correctKey: '#30472f',
    incorrectKey: '#4a292d',
    defaultColor: '#363f4d'
};

let difficulty;
let timeChoice;

[ easy, medium, hard, fifteen, thirty, sixty ].forEach(disableKeyboardActivation);

let testString = [];

/*
 * Runs on load, calls setDefaultModes and initializeApp
 */
window.onload = function() {
    setDefaultModes();
    initializeApp();
}

/*
 * Declares default difficulty and time modes as well as typingIndex
 */
function setDefaultModes() {
    let typingIndex = 0;
    difficulty = LEVELS.easy;
    timeChoice = TIME_OPTIONS.fifteen;
}

/*
 * Initializes main app functions including, button listeners, default button choices, default timer choice, and words in the typing area
 */ 
function initializeApp() {
    initializeLevelListeners();
    initializeTimeListeners();
    toggleDefaults();
    setTimer(15);
    loadWords(LEVELS.easy);
}

/*
 * Changes the color of difficulty and time buttons upon click
 */
function toggleDefaults () {
    fifteen.classList.toggle('active');
    easy.classList.toggle('active');
}

/*
 * Handles button listeners for difficulty buttons.
 * upon click calls setDifficulty and toggleButtonColor
 */
function initializeLevelListeners() {
    [easy, medium, hard].forEach(level => {
        level.addEventListener('click', () => {
            setDifficulty(level);
            toggleButtonColor(level, [easy, medium, hard]);
        });
    });
}

/*
 * Handles button listeners for time buttons.
 * upon click calls setTime and toggleButtonColor
 */
function initializeTimeListeners() {
    [fifteen, thirty, sixty].forEach(timeSelection => {
        timeSelection.addEventListener('click', () => {
            setTime(timeSelection);
            toggleButtonColor(timeSelection, [fifteen, thirty, sixty])
        });
    });
}

/*
 * Receives time as parameter from button listener.
 * updates the timeChoice variable and time displayed
 */
function setTime(timeSelection) {
    switch(timeSelection) {
        case fifteen:
            timeChoice = TIME_OPTIONS.fifteen;
            setTimer(15);
            break;
        case thirty:
            timeChoice = TIME_OPTIONS.thirty;
            setTimer(30);
            break;
        case sixty:
            timeChoice = TIME_OPTIONS.sixty;
            setTimer(60);
            break;
        default:
            timeChoice = TIME_OPTIONS.fifteen;
            setTimer(15);
            break;
    }
}

/*
 * Receives difficulty as parameter from button listener.
 * updates the difficulty variable and difficulty displayed
 */
function setDifficulty(level) {
    switch(level) {
        case easy:
            difficulty = LEVELS.easy;
            break;
        case thirty:
            difficulty = LEVELS.medium;
            break;
        case sixty:
            difficulty = LEVELS.hard;
            break;
        default:
            difficulty = LEVELS.easy;
            break;
    }

    loadWords(difficulty);
}

/*
 * Deactivates all buttons when one is clicked, activates selected button
 */
function toggleButtonColor(buttonSelection, buttonGroup) {
    buttonGroup.forEach(button => button.classList.remove('active'));
    buttonSelection.classList.add('active');
}

/*
 * Passes difficulty choice to backend
 * Receives a set of words based on difficulty. Updates currentWords variable and displays text contents.
 */
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
        let currentWords = data.wordsString;
        console.log ("words:", data);
        const displayText = document.getElementById('display-text');
        displayText.textContent = data.wordsString;
    })
    .catch (error => {
        console.error ('error getting words', error);
    });
}

/*
 * Checks if timer is currently running, if it is clears that interval. 
 * Sets on screen timer to display time variable passed. Every 1000 ms decreases the timer by one.
 */
function startTimer (time) {
    let timerInterval = null;
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

/*
 * Sets the on screen timer to equal time variable passed in.
 */
function setTimer (time) {
    const timer = document.getElementById('timer');
    let timerTime = time;
    timer.textContent = timerTime;
}

document.addEventListener ('keyup', keyPressed);

/*
 * Handles a key being pressed. If the key is enter, begins the test, if the key is backspace, calls handleBackspace, and if the key is a character, calls handleCharacter.
 */
function keyPressed(event) {
    if (event.key === 'Enter') {
        startTest();
    }
    else if (event.key === 'Backspace') {
        handleBackspace();
    }
    else {
        handleCharacter(event.key);
    }
}

function startTest () {
    typingIndex = 0;
    refreshTestString();
    getTextField();
    startTimer(timeChoice);
}
/*
 * Handles a character being pressed. Receives a character that was clicked as the parameter.
 * Splits the current words displayed into array of characters. If the character pressed equals the expected character, show green, if else, show red. 
 * Incriments the typingIndex variable by one and updates the text field.
 */
function handleCharacter(inputChar) {
    const characterArray = currentWords.split("");

    if (inputChar === characterArray[typingIndex]) {
        changeCharacterColor(typingIndex, COLORS.correctKey);
    }
    else {
        changeCharacterColor(typingIndex, COLORS.incorrectKey);
    }

    typingIndex++;
    getTextField();
}

function handleBackspace () {
    typingIndex--;
    removeCharacterColor(typingIndex);
    getTextField();
}

function removeCharacterColor (index) {
    const char = currentWords[index];
    testString[index] = `<span style="color:${COLORS.defaultColor};">${char}</span>`;
}

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

function disableKeyboardActivation(button) {
    button.addEventListener('keydown', function(event) {
        if (event.key === ' ' || event.key === 'Enter') {
            event.preventDefault();  
        }
    });
}
    



    


 
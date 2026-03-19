// Global variables to store current problem
let currentN1 = null;
let currentN2 = null;

// Function to fetch random numbers from the backend
async function fetchRandomNumbers() {
    try {
        const response = await fetch('/number');
        if (!response.ok) {
            throw new Error('Failed to fetch numbers');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching numbers:', error);
        return null;
    }
}

// Function to check answer using the /product endpoint
async function checkAnswer(n1, n2, userAnswer) {
    try {
        const response = await fetch(`/product?n1=${n1}&n2=${n2}`);
        if (!response.ok) {
            throw new Error('Failed to check answer');
        }
        const correctAnswer = await response.json();
        return parseInt(userAnswer) === correctAnswer;
    } catch (error) {
        console.error('Error checking answer:', error);
        return false;
    }
}

// Function to update the problem display with animation
function updateProblemDisplay(n1, n2) {
    const problemElement = document.getElementById('problem');
    problemElement.textContent = `${n1} × ${n2} = ?`;

    problemElement.classList.add('bounce');
    setTimeout(() => {
        problemElement.classList.remove('bounce');
    }, 500);
}

// Function to show feedback
function showFeedback(message, type) {
    const feedbackElement = document.getElementById('feedback');
    feedbackElement.textContent = message;
    feedbackElement.className = `feedback ${type}`;

    // Clear feedback after 3 seconds (except correct message)
    if (type !== 'correct') {
        setTimeout(() => {
            feedbackElement.textContent = '';
            feedbackElement.className = 'feedback';
        }, 3000);
    }
}

// Function to handle new problem
async function handleNewProblem() {
    const data = await fetchRandomNumbers();

    if (data) {
        currentN1 = data.n1;
        currentN2 = data.n2;

        updateProblemDisplay(currentN1, currentN2);

        // Clear input + feedback
        document.getElementById('answer-input').value = '';
        document.getElementById('feedback').textContent = '';
        document.getElementById('feedback').className = 'feedback';
    } else {
        showFeedback("Oops! Couldn't load a new problem. Try again!", 'warning');
    }
}

// Function to handle checking the answer
async function handleCheckAnswer() {
    const answerInput = document.getElementById('answer-input');
    const userAnswer = answerInput.value.trim();

    if (!userAnswer) {
        showFeedback('Please enter an answer first!', 'warning');
        return;
    }

    if (currentN1 === null || currentN2 === null) {
        showFeedback('No problem loaded yet!', 'warning');
        return;
    }

    const isCorrect = await checkAnswer(currentN1, currentN2, userAnswer);

    if (isCorrect) {
        showFeedback('🎉 Fantastic! You got it right! 🎉', 'correct');
    } else {
        const correctAnswer = currentN1 * currentN2;
        showFeedback(`Not quite! The answer is ${correctAnswer}. Try another problem!`, 'incorrect');
    }
}

// Function to reveal answer
async function handleRevealAnswer() {
    if (currentN1 === null || currentN2 === null) {
        showFeedback('No problem loaded yet!', 'warning');
        return;
    }

    try {
        const url = `/product?n1=${currentN1}&n2=${currentN2}`;
        console.log("Calling:", url);

        const response = await fetch(url);
        console.log("Status:", response.status);

        const text = await response.text();  // 👈 important
        console.log("Raw response:", text);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const correctAnswer = JSON.parse(text);

        showFeedback(`The answer is ${correctAnswer}!`, 'correct');

    } catch (error) {
        console.error('FULL ERROR:', error);
        showFeedback("Oops! Couldn't reveal the answer. Try again!", 'warning');
    }
}

// Function to handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        handleCheckAnswer();
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', async function () {
    // Load first problem
    await handleNewProblem();

    // Get elements
    const newProblemBtn = document.getElementById('new-problem-btn');
    const checkAnswerBtn = document.getElementById('check-answer-btn');
    const revealAnswerBtn = document.getElementById('reveal-answer-btn');
    const answerInput = document.getElementById('answer-input');

    // Event listeners
    if (newProblemBtn) {
        newProblemBtn.addEventListener('click', handleNewProblem);
    }

    if (checkAnswerBtn) {
        checkAnswerBtn.addEventListener('click', handleCheckAnswer);
    }

    if (revealAnswerBtn) {
        revealAnswerBtn.addEventListener('click', handleRevealAnswer);
    }

    if (answerInput) {
        answerInput.addEventListener('keypress', handleKeyPress);
    }
});
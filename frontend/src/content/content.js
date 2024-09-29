// content.js
/*global chrome*/

(() => {
    console.log("IIFE in content script executing");
    console.log("content.js script is injected");
    let cur_problem = "";

    // Get the current problem directly from the URL
    function getCurrentProblem() {
        const url = window.location.href;
        const match = url.match(/\/problems\/([^\/]+)\//);
        if (match && match[1]) {
            cur_problem = match[1];
            console.log("Current problem:", cur_problem);
            attachSubmitListener();
        } else {
            console.log("Not on a problem page.");
        }
    }

    getCurrentProblem(); // Initialize the current problem and attach the listener

    // Function to create a listener for submit clicks
    function attachSubmitListener() {
        const submitButtonSelector = 'button[data-e2e-locator="console-submit-button"]';

        function tryAttachListener() {
            const submitButton = document.querySelector(submitButtonSelector);

            if (submitButton) {
                submitButton.removeEventListener('click', handleSubmission);
                submitButton.addEventListener('click', handleSubmission);
                console.log("Submit button listener attached.");
                return true;
            } else {
                console.log("Submit button not found. Waiting for it to become available.");
                return false;
            }
        }

        if (!tryAttachListener()) {
            // If the submit button isn't found, observe the DOM for changes
            const observer = new MutationObserver((mutations, obs) => {
                if (tryAttachListener()) {
                    // Once the submit button is found and listener is attached, stop observing
                    obs.disconnect();
                }
            });

            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    async function handleSubmission() {
        const submitButtonSelector = 'button[data-e2e-locator="console-submit-button"]';
        const submitButton = document.querySelector(submitButtonSelector);

        let count = 0;
        const observer = new MutationObserver(async (mutationsList, observer) => {
            count += 1;
            if (count === 2) {
                await sleep(500); // Wait for elements to load
                const acceptElement = document.querySelector('span[data-e2e-locator="submission-result"]');
                const isAccepted = acceptElement && acceptElement.textContent === 'Accepted';

                observer.disconnect();
                count = 0;

                // Only handle if the submission is accepted
                if (isAccepted) {
                    console.log('Submission accepted.');
                    handleAccepted();
                } else {
                    console.log('Submission not accepted. No further action.');
                    // Do nothing if rejected
                    return;
                }
            }
        });

        observer.observe(submitButton, { attributes: true, subtree: true });
    }

    async function handleAccepted() {
        // Create and show the modal
        const modal = createDifficultyModal();
        document.body.appendChild(modal);

        // Wait for the user to submit the difficulty rating
        const difficulty = await new Promise((resolve) => {
            const submitButton = modal.querySelector('.submit-button');
            const stars = modal.querySelectorAll('.star-btn');
            let selectedDifficulty = 0;

            stars.forEach((star) => {
                star.addEventListener('click', () => {
                    selectedDifficulty = parseInt(star.getAttribute('data-rating'));
                    updateStars(stars, selectedDifficulty);
                    submitButton.disabled = false;
                    submitButton.style.backgroundColor = '#2d3748';
                    submitButton.style.cursor = 'pointer';
                });
            });

            submitButton.addEventListener('click', () => {
                if (selectedDifficulty > 0) {
                    document.body.removeChild(modal);
                    resolve(selectedDifficulty);
                }
            });
        });

        console.log('Difficulty rating entered:', difficulty);

        // Get the username from the page or storage
        let usernameElement = document.querySelector('div[class*="truncate text-text-primary"]');
        let username = usernameElement ? usernameElement.textContent : "";

        if (!username) {
            const result = await chrome.storage.local.get(['username']);
            username = result.username || window.prompt("Enter your LeetCode username:");
            if (username) {
                await chrome.storage.local.set({ username });
            } else {
                console.log("Username not provided.");
                return;
            }
        }

        console.log("Username is:", username);

        // Add problem to the database with accepted status as true
        add_problem(username, cur_problem, difficulty, true);
    }

    // Helper function to add problem data to the backend
    async function add_problem(username, problem_name, difficulty, accepted) {
        try {
            console.log('Sending request to backend...');
            const response = await fetch('http://127.0.0.1:8000/add_problem/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    problem_name,
                    difficulty,
                    accepted
                }),
                credentials: 'include',
            });

            console.log('Response status:', response.status);
            const responseText = await response.text();
            console.log('Response from backend:', responseText);
        } catch (error) {
            console.error('Error sending data to backend:', error);
            console.error('Error details:', error.message);
            if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
                console.error('This might be due to CORS issues or the server not running.');
            }
        }
    }

    // Sleep function for delays
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function createDifficultyModal() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            font-family: Arial, sans-serif;
        `;

        modal.innerHTML = `
            <div style="
                background-color: #2d3748;
                margin: 15% auto;
                padding: 20px;
                border-radius: 8px;
                width: 300px;
                max-width: 80%;
            ">
                <h2 style="
                    margin: 0 0 20px 0;
                    font-size: 1.25rem;
                    color: #fff;
                ">Rate the question difficulty</h2>
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-bottom: 15px;
                ">
                    <button class="star-btn" data-rating="1" style="
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 24px;
                        color: #718096;
                        transition: color 0.2s;
                    ">★</button>
                    <button class="star-btn" data-rating="2" style="
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 24px;
                        color: #718096;
                        transition: color 0.2s;
                    ">★</button>
                    <button class="star-btn" data-rating="3" style="
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 24px;
                        color: #718096;
                        transition: color 0.2s;
                    ">★</button>
                    <button class="star-btn" data-rating="4" style="
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 24px;
                        color: #718096;
                        transition: color 0.2s;
                    ">★</button>
                    <button class="star-btn" data-rating="5" style="
                        background: none;
                        border: none;
                        cursor: pointer;
                        font-size: 24px;
                        color: #718096;
                        transition: color 0.2s;
                    ">★</button>
                </div>
                <p style="
                    text-align: center;
                    color: #a0aec0;
                    font-size: 0.875rem;
                    margin-bottom: 15px;
                ">1 (Easiest) to 5 (Hardest)</p>
                <button class="submit-button" style="
                    display: block;
                    width: 100%;
                    padding: 10px;
                    background-color: #4a5568;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: background-color 0.2s;
                " disabled>Submit</button>
            </div>
        `;

        return modal;
    }

    function updateStars(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.style.color = '#f6e05e';
            } else {
                star.style.color = '#718096';
            }
        });
    }
})();

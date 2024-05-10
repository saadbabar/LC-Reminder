async function fetchData() {
    try {
        // make api request access
        const response = await fetch('https://alfa-leetcode-api.onrender.com/saadbabar/acSubmission');


        // check if response is ok

        if(!response.ok) {
            throw new Error('Network Error')
        }

        // Parsing JSON 

        const data = await response.json();

        // Process Data
        console.log(data);
    }

    catch (error) {
        console.error('Error Fetching Data: ', error);
    }
}

// Function call
fetchData();

// script.js - JavaScript to handle username input and storage

document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById('usernameInput');
    const saveButton = document.getElementById('saveButton');

    // Load saved username if exists
    chrome.storage.sync.get(['leetcodeUsername'], function (result) {
        if (result.leetcodUsername) {
            usernameInput.value = result.leetcodUsername;
        }
    });

    saveButton.addEventListener('click', function () {
        const username = usernameInput.value.trim();
        if (username) {
            // Save username to storage
            chrome.storage.sync.set({ 'leetcodeUsername': username }, function () {
                console.log('LeetCode username saved:', username);
            });
        }
    });
});
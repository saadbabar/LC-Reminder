// content.js


<<<<<<< HEAD
// function getUsername() {
//   event.preventDefault();
//   var userName = document.getElementById('usernameinput').value;
//   // Do something with the user input, such as sending it to your API
//   console.log(userName)
//   document.getElementById('output').innerText = 'You entered: ' + userName;
// }


// // Listen for messages from the background script
// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
// // Check the message action
// if (message.action === "showPopup") {
//   // Your code to show the popup
//   alert("Submit button clicked on LeetCode!");
// }
// })

=======
>>>>>>> 043af45eb7f04feaa8d702127b1f0c75e29a2d5e

(() => {
  console.log("content.js script is injected");


  let cur_problem = "";
  let submitButtonElement = 'button[data-e2e-locator="console-submit-button"]';
  chrome.runtime.onMessage.addListener(handleMessage);
  
  
  function handleMessage(obj, sender, response) {
    const { type, problem } = obj;
    if (type === "ACTIVE PROBLEM") {
      cur_problem = problem;
      attachSubmitListener();
    }
    // chrome.runtime.onMessage.removeListener(handleMessage); ) 
    console.log(`problem: ${problem}`);
    sendMessage({ type: type, problem: problem }); // dummy response so shit doesnt bitch  <--- D1 comment google hire this guy
  }

  // Function creates a listener for submit clicks
  function attachSubmitListener() {
      const submitButton = document.querySelector(submitButtonElement);

      if (submitButton) {
        submitButton.removeEventListener('click', handleSubmission);
        submitButton.addEventListener('click', handleSubmission);
      }
  }

  async function handleSubmission() {
    const submitButton = document.querySelector(submitButtonElement);

    count = 0; 
    async function callback(changeRecords, observer) {
      count += 1;
      if (count == 2) {
        await sleep(500); // idk how to completely get rid of waiting, 'accept' elements not fully loaded in when this executes
        const acceptElement = document.querySelector('span[data-e2e-locator="submission-result"]');
        const isAccepted = acceptElement && acceptElement.textContent === 'Accepted';
        
        if (!acceptElement || !isAccepted) { // rejected submission, dont do anything
          console.log('better together! keep a growth mindset 😘 👨‍❤️‍👨');
          return;
        }
        console.log(acceptElement.textContent);
        
        observer.disconnect();
        count = 0;
        handleAccepted();
      }
    }
    
    const options = {
      attributes: true,
      subtree: true,
    };

    const observer = new MutationObserver(callback);
    observer.observe(submitButton, options);
 }

  function handleAccepted() {
    let difficulty = window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3"); // easiest for now, later we can add a modal
    difficulty = Number(difficulty)
    while (!(1 <= difficulty && difficulty <= 5)) {
      window.alert("difficulty must be between 1 and 5!")
      difficulty = Number(window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3")); // easiest for now, later we can add a modal
    }
    console.log('Difficulty rating entered:', difficulty);

    // integrate difficulty w/ backend
  }


   // HELPERS
   function sendMessage(message) {
    chrome.runtime.sendMessage(message);
  }
  // use "await sleep(ms)"
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }



})();
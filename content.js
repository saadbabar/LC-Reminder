// // Inject button onto leetcode page


function getUsername() {
  event.preventDefault();
  var userName = document.getElementById('usernameinput').value;
  // Do something with the user input, such as sending it to your API
  console.log(userName)
  document.getElementById('output').innerText = 'You entered: ' + userName;
}


// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
// Check the message action
if (message.action === "showPopup") {
  // Your code to show the popup
  alert("Submit button clicked on LeetCode!");
}
})


(() => {
let cur_problem = "";

/*
  Gets message from background script, alerting that we're on a current problem

  Message types (type):
    - ACTIVE PROBLEM: attaches a listener for the submit button
    ...
*/
chrome.runtime.onMessage.addListener((obj, sender, response) => {
  const { type, problem } = obj;

  if (type === "ACTIVE PROBLEM") {
    cur_problem = problem;
    attachSubmitListener();
  }
});

// Function creates a listener for submit clicks
function attachSubmitListener() {
  const submitButton = document.querySelector('button[data-e2e-locator="console-submit-button"]'); 

  submitButton.removeEventListener('click', handleSubmit); // sanity
  submitButton.addEventListener('click', handleSubmit);
}

function handleSubmit() {
    console.log(`${cur_problem} submitted`);
    // check if submit was accepted, if so, modify dom to add the difficulty popup
    // am hella lazy so i'll do this tmrw
}

})()
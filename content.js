// // Inject button onto leetcode page

//gets current url: from stackoverflow 
//https://stackoverflow.com/questions/1979583/how-can-i-get-the-url-of-the-current-tab-from-a-google-chrome-extension
const getLastFocusedWindowUrl = async() =>  {
    // see the note below on how to choose currentWindow or lastFocusedWindow
    const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
    console.log(tab.url);
    return tab.url;
  }

(async () => {
    const currentURL = await getLastFocusedWindowUrl()
    if (currentURL.includes("leetcode.com")) {
        console.log("we are on leetcode right now")
        chrome.runtime.sendMessage({ action: "showPopup" }, function(response) {
            if (chrome.runtime.lastError) {
              console.error("Error sending message:", chrome.runtime.lastError.message);
            } else {
              console.log("Message sent successfully!");
            }
          });
          
    } else {
        console.log("we are not on leetcode")
    }    
})()



const button = document.createElement('button');
button.textContent = 'Click here';
document.body.appendChild(button);

//send message to background script when button is clicked

button.addEventListener('click', () => {
    chrome.runtime.sendMessage({action: 'buttonClicked'});
});

// gets user input from the form
document.getElementById('myForm').addEventListener('submit', getUsername);

function getUsername() {
    event.preventDefault();
    var userName = document.getElementById('usernameinput').value;
    // Do something with the user input, such as sending it to your API
    console.log(userName)
    document.getElementById('output').innerText = 'You entered: ' + userName;
   
}


// injecting code into leetcode webpage, for when user clicks submit

document.addEventListener('DOMContentLoaded', function() {
  //find submit button on leetcode page and attach an event listener

  const lcSubmitButton = document.querySelector('console-submit-button');
  lcSubmitButton.addEventListener('click', function() {
    //send message to background script

    chrome.runtime.sendMessage({action: 'showPopup'})
  })
})


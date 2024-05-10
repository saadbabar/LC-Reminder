// Inject button onto leetcode page

const button = document.createElement('button');
button.textContent = 'Click here';
document.body.appendChild(button);

//send message to background script when button is clicked

button.addEventListener('click', () => {
    chrome.runtime.sendMessage({action: 'buttonClicked'});
});
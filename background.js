// listen to messages from content script

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action === 'buttonClicked') {
        //add logic here
        console.log('button clicked')
    }
})
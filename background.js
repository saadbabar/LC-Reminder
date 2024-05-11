// listen to messages from content script

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action === 'buttonClicked') {
        //add logic here
        console.log('button clicked')
    }
})

chrome.runtime.onMessage.addListener(async function(message, sender, sendResponse) {
    console.log("this is the onMessage Listener firing")
    if (message.action === "showPopup") {
    //   sendResponse({})
      // add logic to showPopup
    }
});
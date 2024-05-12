/* 
    background.js
    Created: May 9, 2024
    Description:
        Responsible for checking if we're currently on a leetcode problem. Sends a message to the 
        content script, which manages dom manipulation.
    Related Files:
        - content.js: Handles difficulty popup on accepted submissions
        - index.html: Main extension interface that provides a link to next recommended question
*/







/*
    - Fired when URL bards updated
    - Checks if we're on leetcode.com/problems
    - Sends message to the content script with the problem name

    URL form: "leetcode.com/problems/<problem name>/"

    references:
        - tabs.onUpdated: https://developer.chrome.com/docs/extensions/reference/api/tabs#event-onUpdated
        - tabs.sendMessage: https://developer.chrome.com/docs/extensions/reference/api/tabs#method-sendMessage

    ** potential concerns:

    chrome.onUpdated's listeners triggered whenever a url is updated, so whenever we refresh a page, 
    click on a link, etc., this listeners fired. so this listeners gonna be fired a lot. idk if this 
    is a concern tho.

*/
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    
    if (changeInfo.url && changeInfo.url.includes("leetcode.com/problems/") && changeInfo.status === 'complete') {
        console.log("Navigated to a LC problem: ", changeInfo.url);
  
        // Extract the problem name from the URL (might need to error handle??)
        const urlParts = changeInfo.url.split('/');
        const problemIndex = urlParts.indexOf('problems') + 1;
        let problemName = urlParts[problemIndex];
        
        // Send msg to the content script
        chrome.tabs.sendMessage(tabId, {
            type: 'ACTIVE PROBLEM',
            problem: problemName
        });
    }
    // do jack shit when we're not on an active problem
  });// listen to messages from content script
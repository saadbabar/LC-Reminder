// content.js



(() => {
  let cur_problem = "";
  let isListenerAttached = false;

  function sendMessage(message) {
    chrome.runtime.sendMessage(message);
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /*
    Gets message from background script, alerting that we're on a current problem
  
    Message types (type):
      - ACTIVE PROBLEM: attaches a listener for the submit button
      ...
  */
  chrome.runtime.onMessage.addListener(handleMessage);

  function handleMessage(obj, sender, response) {
    const { type, problem } = obj;
    if (type === "ACTIVE PROBLEM") {
      cur_problem = problem;
      attachSubmitListener();
    }
    chrome.runtime.onMessage.removeListener(handleMessage);
    sendMessage({ type: type, problem: problem }) // dummy response so shit doesnt bitch  <--- D1 comment google hire this guy
  }

  // Function creates a listener for submit clicks
  function attachSubmitListener() {
    // if (!isListenerAttached) {
      const submitButton = document.querySelector('button[data-e2e-locator="console-submit-button"]');
      if (submitButton) {
        submitButton.removeEventListener('click', handleSubmit);
        submitButton.addEventListener('click', handleSubmit);
        isListenerAttached = true;
      }
    // }
  }

  async function handleSubmit() {
    sendMessage({ status: "clicked this shit" });
    await sleep(5000);
    document.addEventListener('DOMContentLoaded', () => {
      const acceptStuff = document.querySelector('span[data-e2e-locator="submission-result"]');
      const isAccepted = acceptStuff.textContent === 'Accepted';
      
      if (!acceptStuff || !isAccepted) {
        sendMessage({ msg: 'better together! keep a growth mindset 😘 👨‍❤️‍👨'}); // lame as hell
        return;
      }

      sendMessage({ msg: acceptStuff.textContent });
    });
 }

})()
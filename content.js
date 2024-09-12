// content.js
/*global chrome*/


(() => {
  console.log("content.js script is injected");
  let cur_problem = "";
  let submitButtonElement = 'button[data-e2e-locator="console-submit-button"]';
  chrome.runtime.onMessage.addListener(handleMessage);


  function handleMessage(obj, sender, response) {
    const { type, problem } = obj;
    console.log("message recieved, the type is " + type);
    if (type === "ACTIVE PROBLEM") {
      cur_problem = problem;
      attachSubmitListener();
    }
    // else if (type === "INSTALLED") {
    //   onInstallation();
    //
    // }
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

    let count = 0;
    async function callback(changeRecords, observer) {
      count += 1;
      if (count == 2) {
        await sleep(500); // idk how to completely get rid of waiting, 'accept' elements not fully loaded in when this executes
        const acceptElement = document.querySelector('span[data-e2e-locator="submission-result"]');
        const isAccepted = acceptElement && acceptElement.textContent === 'Accepted';

        if (!acceptElement || !isAccepted) { // rejected submission, dont do anything
          console.log('better together! keep a growth mindset');
          handleRejected();
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

  async function handleRejected() {

    // on rejection page no username element pops up
    // let username = document.querySelector('div[class="truncate text-text-primary dark:text-text-primary max-w-full font-medium"]').textContent;

    // solution prompt user to enter username?
    // Ask for username on installation? use chrome.storage to remember username?
    let username = "";

    const result = await chrome.storage.local.get(['username']);

    if (Object.prototype.hasOwnProperty.call(result, 'username')) {
      username = result.username;
      console.log("chrome.storage.local does have the username " + result.username);
    } else {
      username = window.prompt("Enter LC Username");
      await chrome.storage.local.set({ username: username }).then(() => console.log("value is set"));
    }
    // add to database
    add_problem(username, cur_problem, 0, false);

  }


  async function handleAccepted() {
    let difficulty = window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3"); // easiest for now, later we can add a modal
    difficulty = Number(difficulty)
    // TODO: change range back
     //supposed to be 1 to 5, but making larger for testing purposes
    while (!(1 <= difficulty && difficulty <= 100)) {
      window.alert("difficulty must be between 1 and 5!")
      difficulty = Number(window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3")); // easiest for now, later we can add a modal
    }

    //chrome.tabs.executeScript(null, {file: "modal.js"});
    try {
      await chrome.scripting.executeScript({
          target: { tabId: getCurrentTab() },
          files: ['modal.js']
      });
    }
    catch (err) {
      console.log(err);
    }


    //chrome.runtime.sendMessage({ type: "SHOW_MODAL" });

    //// Wait for the user to enter the difficulty
    //difficulty = await new Promise((resolve) => {
    //    chrome.storage.local.get(['difficulty'], (result) => {
    //        resolve(result.difficulty);
    //    });
    //});

    console.log('Difficulty rating entered:', difficulty);

    // integrate difficulty w/ backend
    let username = document.querySelector('div[class="truncate text-text-primary dark:text-text-primary max-w-full font-medium"]').textContent;
    console.log("username is ", username);

    // updating the database
    add_problem(username, cur_problem, difficulty, true);


  }

  function onInstallation() {
    // abandoning this idea for now, will come back
    const username = window.prompt("Enter Your LeetCode Username");
    chrome.storage.local.set({ username: username }).then(() => console.log("value is set"));
    // can retrieve value w/ `chrome.storage.local.get(["username"]).then((result) => {console.log("Value is " + result.username);});`
    chrome.storage.local.get(["username"]).then((result) => { console.log('Value is ' + result.username); });
  }

  // HELPERS
  function sendMessage(message) {
    chrome.runtime.sendMessage(message);
  }
  // use "await sleep(ms)"
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function add_problem(username, problem_name, difficulty, accepted) {

    const response = await fetch('http://127.0.0.1:8000/add_problem/', {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        problem_name: problem_name,
        difficulty: difficulty,
        accepted: accepted
      }),
    });

    // const result = await response.json();
    let passedValue = await new Response(response.body).text();
    console.log('Response from backend: ', passedValue);

  }
  async function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab.id;
}


})();

// content.js



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
    let username = window.prompt("Enter LC Username");

    const response = await fetch('http://127.0.0.1:8000/add_problem/', {

      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        problem_name: cur_problem,
        difficulty: 0,
		    accepted: false
      }),
    });
	  

  }


  async function handleAccepted() {
    let difficulty = window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3"); // easiest for now, later we can add a modal
    difficulty = Number(difficulty)
    // TODO: change range back
    // supposed to be 1 to 5, but making larger for testing purposes
    while (!(1 <= difficulty && difficulty <= 100)) {
      window.alert("difficulty must be between 1 and 5!")
      difficulty = Number(window.prompt("Enter difficulty 1 (easiest) to 5 (hardest)", "3")); // easiest for now, later we can add a modal
    }
    console.log('Difficulty rating entered:', difficulty);

    // integrate difficulty w/ backend
    let username = document.querySelector('div[class="truncate text-text-primary dark:text-text-primary max-w-full font-medium"]').textContent;
    console.log("username is ", username);

    // updating the database
    const response = await fetch('http://127.0.0.1:8000/add_problem/', {

      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        problem_name: cur_problem,
        difficulty: difficulty,
		    accepted: true
      }),
    });

    // const result = await response.json();
    let passedValue = await new Response(response.body).text();
    console.log('Response from backend: ', passedValue);

    // compute problem reccomendations
    //    1. get all problems
    const response1 = await fetch("http://127.0.0.1:8000/get_all_problems/", {

      method: 'POST',
      
      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify({
        username: username
      })

    });
    passedValue = await new Response(response1.body).text();
    console.log(passedValue)


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

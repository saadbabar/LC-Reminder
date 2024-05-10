async function fetchData() {
    try {
        // make api request access
        const response = await fetch('https://alfa-leetcode-api.onrender.com/:username/acSubmission');


        // check if response is ok

        if(!response.ok) {
            throw new Error('Network Error')
        }

        // Parsing JSON 

        const data = await response.json();

        // Process Data
        console.log(data);
    }

    catch (error) {
        console.error('Error Fetching Data: ', error);
    }
}

// Function call
fetchData();
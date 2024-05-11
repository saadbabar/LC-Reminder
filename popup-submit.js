document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.getElementById('save');
    const difficultySelect = document.getElementById('difficulty');
  
    saveButton.addEventListener('click', function() {
      const difficulty = difficultySelect.value;
      // Save the difficulty to storage
      chrome.storage.local.set({ 'difficulty': difficulty }, function() {
        console.log('Difficulty saved:', difficulty);
      });
    });
  });
import React from 'react';
import './Popup.css'; // Make sure this import exists

function Popup() {
  return (
    <div className="popup-container">
      <h1 className="title">LeetCode Reminder</h1>
      
      <h2 className="section-title">Next Problem</h2>
      <div className="problem">
        <h3 className="problem-title">Two Sum</h3>
        <div className="problem-details">
          <span className="difficulty easy">Easy</span>
          <span className="review-date">Review: 2023-09-30</span>
        </div>
      </div>
      <button className="view-problem">View Problem</button>
      
      <h2 className="section-title">Recent Submission</h2>
      <div className="submission">
        <h3 className="submission-title">Valid Parentheses</h3>
        <div className="submission-details">
          <span className="difficulty easy">Easy</span>
          <span className="status accepted">Accepted</span>
        </div>
      </div>
    </div>
  );
}

export default Popup;
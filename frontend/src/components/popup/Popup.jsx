import React, { useState, useEffect } from 'react';
import './Popup.css';

function Popup() {
  const [problem, setProblem] = useState({
    title: "Two Sum",
    difficulty: "Easy",
    url: "https://leetcode.com/problems/two-sum/",
    nextReview: "2023-09-30"
  });

  const [recentSubmission, setRecentSubmission] = useState({
    title: "Valid Parentheses",
    difficulty: "Easy",
    status: "Accepted"
  });

  useEffect(() => {
    // Fetch data from your backend or chrome.storage
    // This is where you'd update the problem and recentSubmission states
  }, []);

  const openProblem = () => {
    chrome.tabs.create({ url: problem.url });
  };

  const openSettings = () => {
    console.log('Settings clicked');
    // Implement settings functionality
  };

  return (
    <div className="card">
      <div className="card-header">
        <h1 className="card-title">LeetCode Reminder</h1>
      </div>
      <div className="card-content">
        <div className="problem-section">
          <h2>Next Problem:</h2>
          <p>{problem.title}</p>
          <div className="problem-info">
            <span className={`badge ${problem.difficulty.toLowerCase()}`}>{problem.difficulty}</span>
            <span className="review-date">Review: {problem.nextReview}</span>
          </div>
        </div>
        <button onClick={openProblem} className="view-problem-button">
          View Problem
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="external-link"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </button>
        <div className="submission-section">
          <h2>Recent Submission:</h2>
          <p>{recentSubmission.title}</p>
          <div className="submission-info">
            <span className={`badge ${recentSubmission.difficulty.toLowerCase()}`}>{recentSubmission.difficulty}</span>
            <span className={`badge ${recentSubmission.status.toLowerCase()}`}>{recentSubmission.status}</span>
          </div>
        </div>
      </div>
      <div className="card-footer">
        <button onClick={openSettings} className="settings-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="settings-icon"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          <span className="sr-only">Settings</span>
        </button>
      </div>
    </div>
  );
}

export default Popup;
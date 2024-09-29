import React from 'react';
import ReactDOM from 'react-dom';
import Popup from './components/popup/Popup'; // Updated import path
import './index.css'; // Make sure this line is not commented out

ReactDOM.render(
  <React.StrictMode>
    <Popup />
  </React.StrictMode>,
  document.getElementById('root')
);
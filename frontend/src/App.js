// === IMPORTS ===
import React, { useState, useEffect } from 'react';
// React = the core library
// useState = lets us store data that can change (like crowd count)
// useEffect = lets us run code repeatedly (like fetching data every 2 sec)

import './App.css';
// Import our CSS styles


// === MAIN COMPONENT ===
function App() {
  // === STATE VARIABLES ===
  // State = data that can change over time
  // When state changes, React automatically re-renders the UI

  const [crowdData, setCrowdData] = useState({
    people: 0,
    status: "Loading..."
  });
  // useState creates a variable (crowdData) and a function to update it (setCrowdData)
  // Initial value: {people: 0, status: "Loading..."}
  // This displays while we wait for the first API call

  const [lastUpdated, setLastUpdated] = useState("");
  // Stores the time of last update


  // === FETCH DATA FROM BACKEND ===
  const fetchCrowdData = async () => {
    // async = this function does something that takes time (fetching from internet)
    // We have to wait for the response

    try {
      const response = await fetch("http://127.0.0.1:5000/crowd");
      // fetch = built-in JavaScript function to make HTTP requests
      // await = wait for the response before continuing
      // This calls your Flask backend

      const data = await response.json();
      // Convert the response from JSON text → JavaScript object
      // data will be like {people: 10, status: "MEDIUM"}

      setCrowdData(data);
      // Update state with new data
      // React sees state changed → automatically re-renders the UI

      // Update timestamp
      const now = new Date();
      setLastUpdated(now.toLocaleTimeString());
      // toLocaleTimeString() formats time like "10:30:45 PM"

    } catch (error) {
      console.error("Error fetching crowd data:", error);
      // If backend is down or any network error, log it to browser console
      setCrowdData({
        people: 0,
        status: "Error"
      });
    }
  };


  // === RUN FETCH REPEATEDLY ===
  useEffect(() => {
    // useEffect runs code when component loads and whenever dependencies change

    fetchCrowdData();
    // Fetch immediately when page loads (don't wait 2 seconds for first update)

    const interval = setInterval(fetchCrowdData, 2000);
    // setInterval = run fetchCrowdData every 2000 milliseconds (2 seconds)
    // This creates a loop: fetch → wait 2 sec → fetch → wait 2 sec → ...

    return () => clearInterval(interval);
    // CLEANUP: when component is removed from screen, stop the interval
    // Without this, the interval would keep running forever even if you close the page
    // This prevents memory leaks

  }, []);
  // [] = empty dependency array
  // Means: run this useEffect only ONCE when component first loads
  // If we put [crowdData] it would re-run every time crowdData changes (infinite loop!)


  // === DETERMINE COLOR ===
  const getStatusColor = () => {
    // Helper function to return CSS color based on status
    switch(crowdData.status) {
      case "LOW":
        return "#4caf50";    // green
      case "MEDIUM":
        return "#ff9800";    // orange
      case "HIGH":
        return "#f44336";    // red
      default:
        return "#9e9e9e";    // gray (for "Loading..." or "Error")
    }
  };


  // === RENDER UI ===
  return (
    <div className="App">
      {/* className = React's version of HTML class attribute */}
      {/* This div has styles from App.css */}

      <header className="App-header">
        <h1>🏫 Smart Campus Intelligence System</h1>
        <p className="subtitle">Real-time Crowd Monitoring</p>
      </header>

      <div className="dashboard">
        {/* Main content area */}

        <div className="card">
          <h2>👥 People Count</h2>
          <div 
            className="count-display"
            style={{ color: getStatusColor() }}
          >
            {/* style={{}} = inline styles in React */}
            {/* Outer {} = "this is JavaScript code" */}
            {/* Inner {} = JavaScript object for CSS properties */}
            
            {crowdData.people}
            {/* {} in JSX = insert JavaScript value */}
            {/* Displays the actual number from state */}
          </div>
        </div>

        <div className="card">
          <h2>📊 Status</h2>
          <div 
            className="status-badge"
            style={{ 
              backgroundColor: getStatusColor(),
              color: 'white'
            }}
          >
            {crowdData.status}
          </div>
        </div>

        <div className="card info-card">
          <h3>ℹ️ Information</h3>
          <div className="info-item">
            <span className="info-label">Last Updated:</span>
            <span className="info-value">{lastUpdated || "Not yet"}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Update Interval:</span>
            <span className="info-value">Every 2 seconds</span>
          </div>
        </div>

      </div>

      <footer className="footer">
        <p>Built with React + Flask + YOLOv8</p>
      </footer>
    </div>
  );
}

// === EXPORT ===
export default App;
// Makes this component available to other files
// index.js imports this and renders it to the screen
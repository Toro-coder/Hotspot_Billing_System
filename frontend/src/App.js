import './App.css';
import Login from './components/Login';
import React from 'react';
// Importing the background image
import bgImage from './assets/wifi3.jpeg';
function App() {
  return (
    <div   className="App  w-full h-full overflow-x-hidden">
     <div
  className="fixed top-0 left-0 w-full h-full bg-cover bg-center -z-10"
  style={{ backgroundImage: `url(${bgImage})` }}
></div>

      <Login/>
    </div>
  );
}

export default App;

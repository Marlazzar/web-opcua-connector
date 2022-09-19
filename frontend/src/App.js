import './App.css';
import React, { useEffect, useState } from "react";



function App() {
  const [data, setData ] = useState(null);

  useEffect(() => {
    fetch('/home').then((response) => {
      if (!response.ok) {
        throw new Error(
          "http error: status is ${response.status}"
        );
      }
      return response.json();
    })
    .then((acutalData) => console.log(acutalData))
    .catch((err) => console.log(err.message));
  }, []);

  return (
    <div className="App">
      Hello
    </div>
  );
}

export default App;


import React, { Component } from 'react';

export default function countDown() {
    const [counter, setCounter] = React.useState(60);
  
    // Third Attempts
    React.useEffect(() => {
      const timer =
        counter > 0 && setInterval(() => setCounter(counter - 1), 1000);
      return () => clearInterval(timer);
    }, [counter]);
  
    return (
      <div className="countDown">
        <div>Countdown: {counter}</div>
      </div>
    );
  }
  
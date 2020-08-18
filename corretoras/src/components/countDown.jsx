
import React, { Component } from 'react';

export default function CountDown() {
    const [counter, setCounter] = React.useState(14400);
  
    const secondsToHms=(d)=> {
      d = Number(d);
      var h = Math.floor(d / 3600);
      var m = Math.floor(d % 3600 / 60);
      var s = Math.floor(d % 3600 % 60);
  
      
      var  hDisplay =String(h).padStart(2, '0') 
      var mDisplay = String(m).padStart(2, '0') 
      var sDisplay = String(s).padStart(2, '0') 
      return hDisplay.concat(':',mDisplay,':',sDisplay) 
    
    };
    React.useEffect(() => {
      if (counter==0){
        setCounter(14400)
      }
      const timer =counter>0 && setInterval(() => setCounter(counter - 1), 1000);
      return () => clearInterval(timer);
    }, [counter]);
  
    return (
      
        <div>{secondsToHms(counter)}</div>
      
    );
}

  
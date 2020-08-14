import React from 'react';
import logo from './sulamericaLogo.png';
import './App.css';
import './custom.css'
import ListComponent from './components/clasification.jsx'

function App() {
  return (
    <div className="App">
      <div className="container-fluid">
        <div className="row header">
          <div className="col-2">           

            <img src={logo} width="50%"/>


          </div>
          <div className="col-8">           

            
            Tempo de varredura:

          </div>
          <div className="col-2">           

            login:


          </div>
          


        </div>
        <ListComponent></ListComponent>
        {/* <div className="row">


        </div> */}
        
        
      </div>
    </div>
  );
}

export default App;

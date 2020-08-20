import React from 'react';
import logo from './sulamericaLogo.png';
import './App.css';
import './custom.css'
import loginLogo from './icones_gerais/login_interno.svg'
import ListComponent from './components/clasification.jsx'
import PersonAddIcon from '@material-ui/icons/PersonAdd';
import CountDown from './components/countDown.jsx'
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
            <CountDown/>


          </div>
          <div className="col-2">           

            login:
            {/* <PersonAddIcon style={{fontSize:'35px'}}></PersonAddIcon> */}
            <img src={loginLogo} width="40" height="40" style={{marginLeft:'10px'}}></img>


          </div>
          


        </div>
        <ListComponent></ListComponent>
        
        
        
      </div>
    </div>
  );
}

export default App;

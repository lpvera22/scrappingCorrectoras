import React, { Component } from 'react';
import '../custom.css'
import {Button,Divider} from '@material-ui/core'
import InboxIcon from '@material-ui/icons/Inbox';
import ListUrls from './list.jsx'
import AnalyzeForm from './analyzerForm.jsx'
// import axios from 'axios'
class ListComponent extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          urls:[],
          filt:'todo',
          analyzed:""
        };
        this.loadUrls = this.loadUrls.bind(this);
        this.handleClassifyUrl = this.handleClassifyUrl.bind(this);
        
    }
    loadUrls(){
        fetch('http://127.0.0.1:5000/api/urls')
        .then((resp) => resp.json())
        // .then((data)=> console.log(data))
        .then((jsonStr)=>{    
            this.setState({urls:jsonStr})            
        })
    }
    handleClassifyUrl(url, state){
        let data={
            'url':url,
            'state':state
        }
        fetch('http://127.0.0.1:5000/api/urls', {
            method: 'put',
            body: JSON.stringify(data),
            headers: { 'Content-type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {console.log(data); this.loadUrls()}) 
        .catch(err => console.log(err))
        
    }
    

    componentDidMount() {
        
        this.loadUrls()
    }

    handleAnalyzeUrl=(d)=>{
        this.setState({analyzed:d})
    }
        
        
    
    render() { 
        
        return (
            <React.Fragment>
            <div className="row Clasification">

                <div className="col">
                    
                    <Button className={this.state.filt == 'todo' ? "btn-checked" : ""} style={{color:'white',textTransform:'none'}} onClick={()=>{this.setState({filt: 'todo', analyzed: ""})}}>
                        Sem classificação   
                        <InboxIcon style={{ color: ' #3a91fc',fontSize: 40 }}></InboxIcon>
                    </Button>
                </div>
                <div className="col">
                    <Button className={this.state.filt == 'white' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'white', analyzed: ""})}>
                            White List   
                            <InboxIcon style={{ color: 'white',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'green' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'green', analyzed: ""})}>
                        Green List  
                        <InboxIcon style={{ color: '#00bd6d',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'yellow' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'yellow', analyzed: ""})}>
                        Yellow List  
                        <InboxIcon style={{ color: '#fdf200',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'red' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'red', analyzed: ""})}>
                        Red List  
                        <InboxIcon style={{ color: '#ff0000',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'black' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'black', analyzed: ""})}>
                        Black List  
                        <InboxIcon style={{ color: '#807c7c',fontSize: 40 }}></InboxIcon>
                    </Button>
                </div>
                

                
            
            </div>
            <div>            
                <Divider className='Colored' style={{marginBottom: '2%'}}></Divider>
            </div>
            {this.state.analyzed == "" ? 
                <ListUrls l={this.state.urls} filt={this.state.filt} handleThis={this.handleAnalyzeUrl} handleClassifyUrl={this.handleClassifyUrl}></ListUrls> :
                <AnalyzeForm></AnalyzeForm>
            }
            </React.Fragment>
            

          );
    }
    
    
    
}
 
export default ListComponent ;
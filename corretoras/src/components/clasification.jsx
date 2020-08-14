import React, { Component } from 'react';
import '../custom.css'
import {Button,Divider} from '@material-ui/core'
import InboxIcon from '@material-ui/icons/Inbox';
import ListUrls from './list.jsx'
// import axios from 'axios'
class ListComponent extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          urls:[]
        };
    }
    
    componentDidMount() {
        
        fetch(`http://127.0.0.1:5000/api/urls`,{method: "GET",headers: {"Content-Type": "application/json"}
        })
        .then((resp) => resp.ok)
        .then(data=>console.log(data))

        
    
        
        
        
        
    
    render() { 
        return (
            <React.Fragment>
            <div className="row Clasification">

                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                        Sem classificação   
                        <InboxIcon style={{ color: ' #3a91fc',fontSize: 40 }}></InboxIcon>
                    </Button>
                </div>
                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                            White List   
                            <InboxIcon style={{ color: 'white',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                        Green List  
                        <InboxIcon style={{ color: '#00bd6d',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                        Yellow List  
                        <InboxIcon style={{ color: '#fdf200',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                        Red List  
                        <InboxIcon style={{ color: '#ff0000',fontSize: 40 }}></InboxIcon>
                    </Button>

                </div>
                <div className="col">
                    <Button style={{color:'white',textTransform:'none'}}>
                        Black List  
                        <InboxIcon style={{ color: '#807c7c',fontSize: 40 }}></InboxIcon>
                    </Button>
                </div>
                

                
            
            </div>
            <div>
            
                <Divider className='Colored'></Divider>
            </div>
            <ListUrls l={this.state.urls}></ListUrls>
            </React.Fragment>
            

          );
    }
    
    
    
}
 
export default ListComponent ;
import React, { Component } from 'react';
import InboxIcon from '@material-ui/icons/Inbox';
// import List from '@material-ui/core/List';
// import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { Button } from '@material-ui/core';
class ListUrls extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          onClassify: "",
          isClassifying: ""
        };
    }

    // handleClassifyUrl(url, state){
    //     let data={
    //         'url':url,
    //         'state':state
    //     }
    //     fetch('http://127.0.0.1:5000/api/urls', {
    //         method: 'put',
    //         body: JSON.stringify(data),
    //         headers: { 'Content-type': 'application/json' }
    //     })
    //     .then(response => response.json())
    //     .then(data => console.log(data)) 
    //     .catch(err => console.log(err))
        
    // }

    render() { 
        return (
            <div>
                {this.props.l.filter((item) => item.state == this.props.filt ).map((item, index)=> {
                    return <div className="row" style={{backgroundColor:'#2a2a2a', marginBottom: '1%', padding: '1%'}}>
                            <div className="col-8" style={{display: 'flex', paddingLeft:'10%', textAlign: "left", verticalAlign: 'middle'}}>                                
                                {item.domain}
                            </div>
                            {item.state == 'todo' ? 
                                <div className="col-4">
                                    <button type='button' className='btn btn-classify' hidden={this.state.onClassify == item.url} onClick={() => this.setState({onClassify: item.url})}>Classificar</button>
                                    {this.state.isClassifying == item.url?
                                    <p>loading</p>
                                     : 
                                    <div style={{display: "inline"}}  hidden={this.state.onClassify != item.url}> 
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'white'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: 'white' }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'green'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#00bd6d'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'yellow'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#fdf200'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'red'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#ff0000'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'black'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#807c7c'  }}></InboxIcon></button>
                                    </div>
                                    }
                                </div> :
                                <div className="col-4">
                                    <button type='button' className='btn btn-classify' onClick={() => this.props.handleThis(item.url)}>Análise</button>  
                                </div>
                            }
                        </div>

                })}
            </div>
          );
    }
}
 
export default ListUrls;
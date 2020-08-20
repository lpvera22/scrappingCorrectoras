import React, { Component } from 'react';
import InboxIcon from '@material-ui/icons/Inbox';
import ReactShadowScroll from 'react-shadow-scroll';
import ListItemText from '@material-ui/core/ListItemText';
import { Button } from '@material-ui/core';
import whoisLogo from './icon_logo.svg';
import '../custom.css'
class ListUrls extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          onClassify: "",
          isClassifying: ""
        };
    }

    

    render() { 
        return (
            <div className="fixed-content">
                
                {this.props.l.filter((item) => item.state == this.props.filt ).map((item, index)=> {
                    return <div className="row" style={{backgroundColor:'#2a2a2a', marginBottom: '1%', padding: '1%'}}>
                            <div className='col-2'>
                            <a  target="_blank" href={"https://who.is/whois/"+item.domain}  >
                                <img border="0" alt="whois" src={whoisLogo} width="30" height="30"/>
                            </a>

                            </div>
                            <div className="col-6" style={{display: 'flex', paddingLeft:'10%', textAlign: "left", verticalAlign: 'middle'}}>
                                                               
                                {item.domain}
                                

                            </div>
                            
                            {item.state == 'todo' ? 
                                <div className="col-4">
                                    <button type='button' className='btn btn-classify' hidden={this.props.onClassify == item.url} onClick={() => this.props.handleonClassify(item.url)}>Classificar</button>
                                    {this.props.isClassifying == item.url?
                                    <p>loading</p>
                                     : 
                                    <div style={{display: "inline"}}  hidden={this.props.onClassify != item.url}> 
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'white'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: 'white' }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'green'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#00bd6d'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'yellow'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#fdf200'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'red'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#ff0000'  }}></InboxIcon></button>
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'black'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#807c7c'  }}></InboxIcon></button>
                                    </div>
                                    }
                                </div> :

                                <div className="col-4">
                                    <button type='button' className='btn btn-classify' onClick={() => this.props.handleThis(item)}>Análise</button>
                                    <button type='button' className='btn btn-classify' hidden={this.props.onClassify == item.url} onClick={() => this.props.handleonClassify(item.url)}>Re-classificar</button>
                                    {this.props.isClassifying == item.url?
                                    <p>loading</p>
                                     : 
                                    <div style={{display: "inline"}}  hidden={this.props.onClassify != item.url}>
                                        {item.state !== 'white'?
                                            <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'white'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: 'white' }}></InboxIcon></button>
                                            :null
                                        }
                                        {item.state !== 'green'?
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'green'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#00bd6d'  }}></InboxIcon></button>
                                        :null}
                                        {item.state !== 'yellow'?
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'yellow'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#fdf200'  }}></InboxIcon></button>
                                        :null
                                        }
                                        {item.state!=='red'?
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'red'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#ff0000'  }}></InboxIcon></button>
                                        :null}
                                        {item.state!=='black'?
                                        <button className='btn btn-classify' style={{border: 'None'}} onClick={() => {this.props.handleClassifyUrl(item.url, 'black'); this.setState({isClassifying:item.url})}}><InboxIcon style={{ color: '#807c7c'  }}></InboxIcon></button>
                                        :null}
                                        
                                        
                                    </div>
                                    }
                                    
                                </div>
                            }
                            
                        </div>

                })}
                
            </div>
          );
    }
}
 
export default ListUrls;
import React, { Component } from 'react';
import '../custom.css'
import {Button,Divider} from '@material-ui/core'
import InboxIcon from '@material-ui/icons/Inbox';
import ListUrls from './list.jsx'
import AnalyzeForm from './analyzerForm.jsx'
import blueBox from '../icones_gerais/sem_classificacao.svg'
import whiteBox from '../icones_gerais/white_list.svg'
import greenBox from '../icones_gerais/green_list.svg'
import yellowBox from '../icones_gerais/yellow_list.svg'
import redBox from '../icones_gerais/red_list.svg'
import blackBox from '../icones_gerais/black_list.svg'
class ListComponent extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          urls:[],
          filt:'todo',
          analyzed:"",
          isClasifying:'',
          onClassify:''
        };
        this.loadUrls = this.loadUrls.bind(this);
        this.handleClassifyUrl = this.handleClassifyUrl.bind(this);
        this.handleonClassify=this.handleonClassify.bind(this)
        
    }
    loadUrls(){
        fetch('http://161.35.224.138:5000/api/urls')
        .then((resp) => resp.json())
        // .then((data)=> console.log(data))
        .then((jsonStr)=>{
            this.setState({urls:jsonStr})            
        })
    }


    handleClassifyUrl(url, state){
        this.setState({isClasifying:url,onClassify:url})
        let data={
            'url':url,
            'state':state
        }
        fetch('http://161.35.224.138:5000/api/urls', {
            method: 'put',
            body: JSON.stringify(data),
            headers: { 'Content-type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {console.log(data); this.loadUrls();this.setState({isClasifying:'',onClassify:''})}) 
        .catch(err => console.log(err))
        
    }
    
    handleonClassify(url){
        console.log(url)
        this.setState({onClassify:url})

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
                    
                    <Button className={this.state.filt == 'todo' ? "btn-checked" : ""} style={{color:'white',textTransform:'none'}} onClick={()=>{this.setState({filt: 'todo', analyzed: "", onClassify:"",isClasifying:""})}}>
                        <span style={{lineHeight:'150%'}}>Sem classificação
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'todo').length}</span> 
                        </span>
                        <img src={blueBox} width="40" height="40" ></img>
                        {/* <InboxIcon style={{ color: ' #3a91fc',fontSize: 40 }}></InboxIcon> */}
                    </Button>
                </div>
                <div className="col">
                    <Button className={this.state.filt == 'white' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'white', analyzed: "", onClassify:"",isClasifying:""})}>
                        <span style={{lineHeight:'150%'}}>White List
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'white').length}</span> 
                        </span>
                        <img src={whiteBox} width="40" height="40" ></img>
                            {/* <InboxIcon style={{ color: 'white',fontSize: 40 }}></InboxIcon> */}
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'green' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'green', analyzed: "", onClassify:"",isClasifying:""})}>
                        <span style={{lineHeight:'150%'}}>Green List
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'green').length}</span> 
                        </span>
                        <img src={greenBox} width="40" height="40" ></img>
                        {/* <InboxIcon style={{ color: '#00bd6d',fontSize: 40 }}></InboxIcon> */}
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'yellow' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'yellow', analyzed: "", onClassify:"",isClasifying:""})}>
                        <span style={{lineHeight:'150%'}}>Yellow List
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'yellow').length}</span> 
                        </span>
                        <img src={yellowBox} width="40" height="40" ></img>
                        {/* <InboxIcon style={{ color: '#fdf200',fontSize: 40 }}></InboxIcon> */}
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'red' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'red', analyzed: "", onClassify:"",isClasifying:""})}>
                        <span style={{lineHeight:'150%'}}>Red List
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'red').length}</span> 
                        </span>
                        <img src={redBox} width="40" height="40" ></img>
                        {/* <InboxIcon style={{ color: '#ff0000',fontSize: 40 }}></InboxIcon> */}
                    </Button>

                </div>
                <div className="col">
                    <Button className={this.state.filt == 'black' ? "btn-checked" : ""}  style={{color:'white',textTransform:'none'}} onClick={()=>this.setState({filt: 'black', analyzed: "", onClassify:"",isClasifying:""})}>
                        <span style={{lineHeight:'150%'}}>Black List
                            <br></br>
                            <span style={{fontSize:'15px', color: 'gray'}}>{this.state.urls.filter((item) => item.state === 'black').length}</span> 
                        </span>
                        <img src={blackBox} width="40" height="40" ></img>
                        {/* <InboxIcon style={{ color: '#807c7c',fontSize: 40 }}></InboxIcon> */}
                    </Button>
                </div>
                

                
            
            </div>
            <div>            
                <Divider className='Colored' style={{marginBottom: '2%', background:'#807c7c'}}></Divider>
            </div>
            {this.state.analyzed == "" ? 
                <ListUrls l={this.state.urls} filt={this.state.filt} handleThis={this.handleAnalyzeUrl} handleClassifyUrl={this.handleClassifyUrl} isClassifying={this.state.isClasifying} handleonClassify={this.handleonClassify} onClassify={this.state.onClassify}></ListUrls> :
                <AnalyzeForm item={this.state.analyzed}></AnalyzeForm>
            }
            </React.Fragment>
            

          );
    }
    
    
    
}
 
export default ListComponent ;
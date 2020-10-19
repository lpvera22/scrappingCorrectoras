import React, { Component } from 'react';
import '../custom.css'
import {Button} from '@material-ui/core'
import CreateIcon from '@material-ui/icons/Create';
import DescriptionIcon from '@material-ui/icons/Description';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
import Divider from '@material-ui/core/Divider';
import creatLogo from '../icones_gerais/lapis_pagina_criar_anotacao.svg'
import detailLogo from '../icones_gerais/folha_anotacoes.svg'
class AnalyzerForm extends Component {
    constructor (props) {
        super(props);
        
        this.state = {
            clicked: "textual",
            keywords: [], 
            imgUrls: [], 
            addAnot:'',
            title:'',
            content:'', 
            see:'',
            commentToShow:''

        }
    }
    componentDidMount() {        
        this.setState({keywords: this.extractKeywords()});
        this.extractImgUrls()
    }
    extractImgUrls(){
        let data={
            'domain':this.props.item.domain,
            
            
            
        }
        console.log('DATAAAAAA',data)
        fetch('http://161.35.224.138:5000/api/images/?' + new URLSearchParams(data))        
        .then(response => {
            if (response.status==404){
                return {content:'Sem anotações'}

            }
            return response.json();
        })
        .then(data => {
            this.setState({imgUrls:data}) ;console.log('IMGURLS',data)}) 
        .catch(err => console.log(err))

    }
    extractKeywords(){
        if (typeof this.props.item.keywords == 'number' ||typeof this.props.item.keywords == 'undefined'  )
            return []
        let res = this.props.item.keywords.split(',');
        return res;
    }
    updateInputValue(evt) {
        this.setState({
          title: evt.target.value
        });
        console.log(this.state.title)
      }
    handleOnSent(){
        
        let data={
            'domain':this.props.item.domain,
            'title':this.state.title,
            'content':this.state.content,
            'resource':this.state.addAnot
            
        }
        console.log('DATA TO SAVE',data)
        fetch('http://161.35.224.138:5000/api/anotacao/', {
            method: 'post',
            body: JSON.stringify(data),
            headers: { 'Content-type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {console.log(data); this.setState({addAnot:''})}) 
        .catch(err => console.log(err))
        
    }
    updateContentValue(evt){
        this.setState({
            content: evt.target.value
          });
          console.log(this.state.content)


    }
    loadComment(resource){
        let data={
            'domain':this.props.item.domain,
            
            'resource':resource
            
        }
        // console.log('DATAAAAAA',data)
        fetch('http://161.35.224.138:5000/api/anotacao/?' + new URLSearchParams(data))        
        .then(response => {
            if (response.status==404){
                return {content:'Sem anotações'}

            }
            return response.json();
        })
        .then(data => {
            this.setState({commentToShow:data}) ;console.log(data)}) 
        .catch(err => console.log(err))

    }
    

    render() { 
        return (
            <div>
                <div className='row' style={{backgroundColor:'#2a2a2a', paddingTop:'20px',paddingBottom:'20px', fontSize:''}}>
                    <div style={{width:'100%'}}>
                        {this.props.item.domain}
                    </div>
                </div>
                <div className='row'>
                    <div style={{width:'100%', marginTop:'3%', marginBottom:'1%'}}>
                        <Button className={this.state.clicked == 'textual' ? "btn-checked-sub" : ""} style={{color:'white',textTransform:'none', fontSize: 20}} onClick={()=>{this.setState({clicked: 'textual',addAnot:'',see:''})}}>Textual</Button>
                        <Button className={this.state.clicked == 'visual' ? "btn-checked-sub" : ""} style={{color:'white',textTransform:'none', fontSize: 20}} onClick={()=>{this.setState({clicked: 'visual',addAnot:'',see:''})}}>Visual</Button>
                    </div>
                </div>
                <div className='row'>
                    <div className='col-8 fixed-content'>
                        {this.state.clicked == "textual" ? 
                            this.state.keywords.map(value => {
                                    return <div className='row d-flex' style={{backgroundColor:'#2a2a2a', marginBottom: '1%', padding: '1.5%', paddingLeft: '10%'}}>
                                        <div className="mr-auto p-2">{value}</div>
                                        <button className="btn btn-anotacoes p-2" value={value} onClick={()=>{this.setState({addAnot:{value}});console.log(this.state.addAnot)}} >
                                            {/* <img src={creatLogo} width="40" height="40" style={{marginLeft:'10px'}}></img> */}
                                            <CreateIcon></CreateIcon>

                                        </button>
                                        <button className="btn btn-anotacoes p-2" value={value} onClick={()=>{this.loadComment(value); this.setState({addAnot:'',see:{value}});}} > <DescriptionIcon></DescriptionIcon> </button>
                                    </div>
                            }) :  this.state.imgUrls.map(value => {
                                    return <div className='row d-flex' style={{backgroundColor:'#2a2a2a', marginBottom: '1%', padding: '1.5%', paddingLeft: '10%'}}>
                                        <div className="mr-auto p-2">
                                            <a target="_blank" rel="noopener noreferrer" href={value.imgSrc}>{value.imgSrc}</a>
                                            {/* <div class="box">
                                                <iframe src={value.imgSrc} frameborder="0" width = '720px' height='560px'>
                                                </iframe>
                                            </div>  */}
                                        </div>                                        
                                        <button className="btn btn-anotacoes p-2" value={value.imgSrc} onClick={()=>{this.setState({addAnot:value.imgSrc});console.log(this.state.addAnot)}} > <CreateIcon></CreateIcon> </button>
                                        <button className="btn btn-anotacoes p-2" value={value.imgSrc} onClick={()=>{this.loadComment(value.imgSrc); this.setState({addAnot:'',see:value.imgSrc});}} > <DescriptionIcon></DescriptionIcon> </button>
                                    </div>                           
                            }) 
                        }                       
                    </div>
                    {this.state.addAnot !==''  ? <div className='col-4 formAddNoteContainer'>
                        <div className='formAddNote'>
                            <form>
                                <label>{this.state.addAnot.value}</label>
                                <div className="form-group">
                                    <input class="form-control form-control-lg" type="text" placeholder="escreva seu titulo" value={this.state.title} onChange={evt => this.updateInputValue(evt)}></input>
                                </div>
                                <div className="form-group">
                                    <textarea class="form-control" id="content" rows="10" placeholder="escreva seu texto" value={this.state.content} onChange={evt => this.updateContentValue(evt)}></textarea>
                                </div>
                                <button type="button" class="btn btn-classify mb-2" style={{float:'left'}} onClick={()=>{this.handleOnSent()}}>salvar</button>
                                <button type="button" class="btn btn-classify mb-2" style={{float:'right'}} onClick={()=>this.setState({addAnot:''})}>Cancel</button>
                            </form>
                        </div>
                    </div>
                    : this.state.see !=='' ? <div className='col-4 formAddNoteContainer'>
                        <div className='formNote'>
                        <span><b>{this.state.see.value}</b></span>
                        {this.state.commentToShow.content !== 'Sem anotações' ?  <div><div className='formNoteTitle'><FiberManualRecordIcon style={{fontSize:'14px'}}></FiberManualRecordIcon> {this.state.commentToShow.title}</div>
                        <Divider style={{background:'#807c7c'}} ></Divider>
                        <div className='formNoteContent'>{this.state.commentToShow.content}</div>
                        <Divider style={{background:'#807c7c'}} ></Divider>
                        <div className='formNoteDate'>Última alteração:{this.state.commentToShow.data}</div></div>
                        : <div className='formNoteContent'>{this.state.commentToShow.content}</div>
                        }
                        </div>
                    </div>
                    : null
                    }
                    
                </div>
            </div>
          );
    }
}
 
export default AnalyzerForm;
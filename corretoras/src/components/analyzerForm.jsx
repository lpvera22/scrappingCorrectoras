import React, { Component } from 'react';
import '../custom.css'
import {Button} from '@material-ui/core'
import CreateIcon from '@material-ui/icons/Create';
class AnalyzerForm extends Component {
    constructor (props) {
        super(props);
        
        this.state = {
            clicked: "textual",
            keywords: []
        }
    }
    componentDidMount() {        
        this.setState({keywords: this.extractKeywords()});
    }

    extractKeywords(){
        if (typeof this.props.item.keywords == 'number')
            return []
        let res = this.props.item.keywords.split(',');
        return res;
    }

    render() { 
        return (
            <React.Fragment>
                <div className='row' style={{backgroundColor:'#2a2a2a', paddingTop:'20px',paddingBottom:'20px', fontSize:''}}>
                    <div style={{width:'100%'}}>
                        {this.props.item.domain}
                    </div>
                </div>
                <div className='row'>
                    <div style={{width:'100%', marginTop:'3%', marginBottom:'1%'}}>
                        <Button className={this.state.clicked == 'textual' ? "btn-checked" : ""} style={{color:'white',textTransform:'none'}} onClick={()=>{this.setState({clicked: 'textual'})}}>Textual</Button>
                        <Button className={this.state.clicked == 'visual' ? "btn-checked" : ""} style={{color:'white',textTransform:'none'}} onClick={()=>{this.setState({clicked: 'visual'})}}>Visual</Button>
                    </div>
                </div>
                <div className='row'>
                    <div className='col-8'>
                        {this.state.clicked == "textual" ? 
                            this.state.keywords.map(value => {
                                return <div className='row d-flex justify-content-between' style={{backgroundColor:'#2a2a2a', marginBottom: '1%', padding: '1.5%', paddingLeft: '10%'}}>
                                    {value}
                                    <button className="btn btn-anotacoes" > <CreateIcon></CreateIcon> criar anotaões</button>
                                </div>
                        }) : 
                            
                        }
                        
                    </div>
                    <div className='col-4'>

                    </div>
                </div>
            </React.Fragment>
          );
    }
}
 
export default AnalyzerForm;
import React, { Component } from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
class ListUrls extends Component {

    state = {  }
    render() { 
        return (
            <List >
                {this.props.l.map(function(val) {
                    return <ListItem style={{backgroundColor:'#2a2a2a'}}> <ListItemText primary={val} /></ListItem>

                })}
                

            </List>

          );
    }
}
 
export default ListUrls;
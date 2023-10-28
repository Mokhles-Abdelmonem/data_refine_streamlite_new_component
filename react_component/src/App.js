import React, { Component } from 'react';
import './App.css';
import MyComponent from './MyComponent';
import { extendTheme } from '@mui/joy/styles';
import DataGridTest from './DataGridCopy';

class App extends Component {
  
  render() {
    return (
      <MyComponent/>
      // <DataGridTest/>
      );
  }
}

export default App;

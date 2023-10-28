import * as React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import SettingsApplicationsIcon from '@mui/icons-material/SettingsApplications';
import { DataGrid, GridColumnMenu } from '@mui/x-data-grid';
import { Streamlit } from "streamlit-component-lib";
import FormDialog from './DialogForm';


export default function DfEvents (props, setOpen, open) {
  const Events = [
    {
    "name":"drop_column",
    "value":"drop column",
    "action":() => {
      Streamlit.setComponentValue({colName: props.colDef.field, event: "drop_column"});
    },
    },
    {
    "name":"drop_null_col",
    "value":"drop column with nulls",
    "action":() => {
      Streamlit.setComponentValue({colName: props.colDef.field, event: "drop_null_col"});
    },
    },
    {
    "name":"drop_null_row",
    "value":"drop rows with nulls",
    "action":() => {
      console.log("setOpen");
      console.log(setOpen);
      setOpen(true);
      
      // Streamlit.setComponentValue({colName: props.colDef.field, event: "drop_null_row"});
    },
    },
  ]
  return Events
}

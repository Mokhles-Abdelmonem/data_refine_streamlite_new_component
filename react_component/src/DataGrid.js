import * as React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import SettingsApplicationsIcon from '@mui/icons-material/SettingsApplications';
import { DataGrid, GridColumnMenu } from '@mui/x-data-grid';
import { Streamlit } from "streamlit-component-lib";
import FormDialog from './DialogForm';
import DfEvents from './Events';
import Menu from "@mui/material/Menu";
import { NestedMenuItem } from "mui-nested-menu";
import TextField from '@mui/material/TextField';
import ListMenu from './Menu';


function CustomUserItem(props) {
  let Events = DfEvents()
  function menuItems() {
    const menuItemsWrap = []
    const menuItems = []
    Events.map((event) => {
      const setComponentValue  = props[event.name];
      menuItems.push(
        <MenuItem onClick={setComponentValue}>
            <ListItemIcon>
              <SettingsApplicationsIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>{event.value}</ListItemText>
        </MenuItem>
      )
    });
    menuItemsWrap.push(
      <>
        {ListMenu()}
        {/* {menuItems} */}
      </>
    )
    return menuItemsWrap;   
  }

  return (
    <>
      {menuItems()}
    </>
  );
}

function CustomColumnMenu(props) {

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };


  const itemProps = {
    colDef: props.colDef,
    onClick: props.hideMenu,
  };

  const colName = props.colDef.field;
  const ColumnMenuItems = {displayOrder: 15}
  let Events = DfEvents(props, setOpen, open)


  Events.map(event => {
    ColumnMenuItems[event.name] = event.action
  })

  // console.log("props");
  // console.log(props);
  return (
    <>
      <FormDialog 
      open={open}
      handleClose={setOpen}
      />
      <GridColumnMenu
        {...itemProps}
        {...props}
        slots={{
          // Add new item
          columnMenuUserItem: CustomUserItem,
        }}
        slotProps={{
          columnMenuUserItem: ColumnMenuItems,
        }}
        />
    </>
  );
}


export default function CustomDataGrid ({columns, rows}) {


  const RefinedCols = [];
  columns.forEach(element => {
    RefinedCols.push({"field" : element});
  });

  const Rows =  Object.values(JSON.parse(rows));
  const RefinedRows =  []
  Rows.forEach(function (row, index) {
    row["id"] = index;
    RefinedRows.push(row);
  });


  return (
    <div style={{ height: 400, width: '100%' }}>

      <DataGrid
      columns={RefinedCols}
      rows={RefinedRows}
      sx={{
        boxShadow: 2,
        border: 2,
        backgroundColor: "var(--joy-palette-primary-100, #E3EFFB)"
      }}
      slots={{ columnMenu: CustomColumnMenu }}
      />
    </div>
  );
}
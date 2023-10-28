import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React from "react";
import CustomDataGrid from "./DataGrid";

class MyComponent extends StreamlitComponentBase {
  constructor(props) {
    super(props);
    this.state = { numClicks: 0, isFocused: false };
  }

  render() {
    const columns = this.props.args["columns"];
    const rows = this.props.args["rows"];
    return (
      <CustomDataGrid
      columns={columns}
      rows={rows}
      />
    );
  }

}

export default withStreamlitConnection(MyComponent);

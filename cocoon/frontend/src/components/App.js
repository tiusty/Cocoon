import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
const App = () => (
  <DataProvider endpoint="http://127.0.0.1:8000/signatures/snippets/"
                render={data => <Table data={data.results} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
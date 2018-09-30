import React from "react";
import DataProvider from "../helpers/DataProvider";
import Table from "../helpers/Table";

const Signatures = () => (
<DataProvider endpoint="http://127.0.0.1:8000/signatures/snippets/"
render={data => <Table data={data.results} />} />
);

export default Signatures

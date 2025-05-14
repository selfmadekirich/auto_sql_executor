import React from "react";
import { Table } from 'react-bootstrap';

import InfiniteScroll from "react-infinite-scroll-component";


export function InfiniteLoopTable({ headers, data, update }) {
  return (
    <InfiniteScroll
      dataLength={data.length}
      next={update}
      hasMore={true}
      loader={<h4></h4>}
    >
     <Table striped bordered hover>
              <thead>
                <tr>
                  {headers.map(key => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, index) => (
                  <tr key={index}>
                    {headers.map(header => (
                      <td key={header}>{row[header]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
    </InfiniteScroll>
  );
}

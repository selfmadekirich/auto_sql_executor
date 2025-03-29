import React, { useState, useEffect } from 'react';
import UserProjectRow from '../components/UserProjectRecord';
import api from '../api'
import { fetchProjects } from '../api/Projects';


function Projects() {

  const [userProjectRows, setUserProjectRows] = useState([]);

  useEffect(() => {
    fetchProjects(setUserProjectRows,
      (error) => {console.error(error)}
     )
  }, []);


  return (
    <div className="container mt-5">
        <div className="d-flex justify-content-start align-items-center mb-4">
        <h2 className="mt-3">Projects</h2>
        </div>
    <table className="table">
      <thead>
        <tr>
          <th className="text-start">Connection Name</th>
          <th>Description</th>
          <th>Db Type</th>
        </tr>
      </thead>
      <tbody className="my-3">
        {userProjectRows.map((row, index) => (
          <UserProjectRow 
            key={index}
            connectionId={row.connection_id}
            connectionName={row.connectionName} 
            description={row.description} 
            dbType={row.dbType} 
          />
        ))}
      </tbody>
    </table>
  </div>
  );
};

export default Projects;
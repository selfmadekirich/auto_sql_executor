import React from 'react';
import UserProjectRow from '../components/UserProjectRecord';

function Projects() {
  // Заглушка для написания фронта
  const UserProjectRows = [
    { connectionName: "connection_1", description: "description_1", dbType: "PostgreSQL" },
    { connectionName: "connection_2", description: "description_2", dbType: "MySQL" },
    { connectionName: "connection_3", description: "description_3", dbType: "SQLite" },
  ];

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
        {UserProjectRows.map((row, index) => (
          <UserProjectRow 
            key={index}
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
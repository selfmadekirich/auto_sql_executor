import React, {useState } from 'react';
import ConnectionRecord from '../components/ConnectionRecord';
import EditRecordModal from '../components/EditRecordModal';

function Connections() {
     

    const [selectedConnection, setSelectedConnection] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isNewConnectionModalOpen, setIsNewConnectionModalOpen] = useState(false);


    const handleEdit = (connection) => {
        setSelectedConnection(connection);
        setIsModalOpen(true);
    };
    
      const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleNewConnectionCloseModal = () => {
        setIsNewConnectionModalOpen(false);
    };

    const handleDelete = (id) => {
        const updatedConnections = connections.filter(connection => connection.id !== id);
        setConnections(updatedConnections);
    };

      const handleSaveChanges = (updatedConnection) => {
        const updatedConnections = connections.map(connection =>
          connection.id === selectedConnection.id ? updatedConnection : connection
        );
        setConnections(updatedConnections);
        setIsModalOpen(false);
    };


    const handleSaveNewConnection = (newConnection) => {
        const updatedConnections = connections.concat([newConnection])
        setConnections(updatedConnections);
        setIsNewConnectionModalOpen(false);
    };

  const [connections, setConnections] = useState([
    { id: "097f9e10-2d51-4e02-9340-0cb3f6ff6516",connectionName: "connection_1", password:"", description: "description_1", dbName: "test1", host: "127.0.0.1", dbType: "PostgreSQL" },
    { id: "3b5a1680-0685-4358-972b-4c080e0d5906", connectionName: "connection_2",password:"", description: "description_2", dbName: "test1",host: "127.0.0.1", dbType: "MySQL" },
    { id: "3fdbccd6-0bfb-45bb-9c21-8d238ca3c0cb", connectionName: "connection_3",password:"", description: "description_3",dbName: "test1", host: "127.0.0.1", dbType: "SQLite" },
  ])

  return (
    <div className="container mt-5">
        <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mt-3">Connections</h2>
        </div>
        <div className='d-flex justify-content-end mb-4'>
        <button className="btn btn-primary" onClick={() => setIsNewConnectionModalOpen(true)}>Add New</button>
        </div>
    <table className="table">
      <thead>
        <tr>
          <th className="text-start">Connection Name</th>
          <th>Description</th>
          <th>Host</th>
          <th>Db Name</th>
          <th>Db Type</th>
        </tr>
      </thead>
      <tbody className="my-3">
        {connections.map((row, index) => (
          <ConnectionRecord 
            key={index}
            connectionName={row.connectionName} 
            description={row.description} 
            dbType={row.dbType} 
            host={row.host}
            dbName={row.dbName}
            onDelete={ () => {handleDelete(row.id); console.log("delete is pressed")}}
            onEdit={ () => {handleEdit(row)} }

          />
        ))}
      </tbody>
    </table>
    {isModalOpen && (
        <EditRecordModal
          connection={selectedConnection}
          onClose={handleCloseModal}
          onSave={handleSaveChanges}
        />
      )}
      {isNewConnectionModalOpen && (
        <EditRecordModal
          connection={null}
          onClose={handleNewConnectionCloseModal}
          onSave={handleSaveNewConnection}
        />
      )}
  </div>
  );
};

export default Connections;
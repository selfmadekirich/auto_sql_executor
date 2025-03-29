import React, { useState, useEffect } from 'react';
import api from '../api';
import { fetchDb_types } from '../api/Connections';




function EditRecordModal({connection, onClose, onSave }){
  if (connection === null){
    connection = {
      connection_id:"",
      connectionName: "", 
      password:"",
      description: "",
      dbName: "",
      host: "",
      dbType: "",
      user: "",
      port: 0,
      schema_name: ""
    }
  }
  const [formData, setFormData] = useState({
    description: connection.description,
    host: connection.host,
    dbName: connection.dbName,
    dbType: connection.dbType,
    connectionName: connection.connectionName,
    password: "",
    port: connection.port,
    user: connection.user,
    schema_name: connection.schema_name,
    id: connection.connection_id
  });


  const [dbTypes, setDbTypes] = useState([]);

  useEffect(() => {
    fetchDb_types(setDbTypes, 
      (error) => {console.error('Error fetching data:', error)})
  }, []);

  const handleChange = (e) => {
    console.log("here")
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = () => {
    const updatedConnection = {
      ...connection,
      ...formData,
    };
    onSave(updatedConnection);
  };

  return (
    <div className="modal" style={{ display: 'block' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Edit Connection</h5>
          </div>
          <div className="modal-body">
            <form>
              <div className="mb-3">
                <label htmlFor="connectionName" className="form-label d-block text-start">Connection Name</label>
                <input type="text" className="form-control" onChange={handleChange}  id="connectionName" value={formData.connectionName} />
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">DB Type</label>
                <select className="form-select" id="dbType" onChange={handleChange} value={formData.dbType}>
                  <option value="">Select DB Type</option>
                  {dbTypes.map((type, index) => (
                    <option key={index} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="dbName" className="form-label d-block text-start">DB Name</label>
                <input type="text" className="form-control" onChange={handleChange} id="dbName" value={formData.dbName} />
              </div>
              <div className="mb-3">
                <label htmlFor="dbName" className="form-label d-block text-start">Schema name</label>
                <input type="text" className="form-control" onChange={handleChange} id="schema_name" value={formData.schema_name} />
              </div>
              <div className="mb-3">
                <label htmlFor="host" className="form-label d-block text-start">Host</label>
                <input type="text" className="form-control" onChange={handleChange} id="host" value={formData.host} />
              </div>
              <div className="mb-3">
                <label htmlFor="port" className="form-label d-block text-start">Port</label>
                <input type="text" className="form-control" onChange={handleChange} id="port" value={formData.port} />
              </div>
              <div className="mb-3">
                <label htmlFor="user" className="form-label d-block text-start">User</label>
                <input type="text" className="form-control" onChange={handleChange} id="user" value={formData.user} />
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">Password</label>
                <input type="password" className="form-control" onChange={handleChange} id="password" value={formData.password} />
              </div>
              <div className="mb-3">
                <label htmlFor="description" className="form-label d-block text-start">Description</label>
                <input type="text" className="form-control" onChange={handleChange} id="description" value={formData.description} />
              </div>
            </form>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Close</button>
            <button type="button" className="btn btn-primary" onClick={handleSubmit}>Save changes</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EditRecordModal
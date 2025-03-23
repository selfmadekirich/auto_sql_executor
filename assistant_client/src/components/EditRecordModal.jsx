import React, { useState } from 'react';



function EditRecordModal({connection, onClose, onSave }){
  console.log(connection)
  if (connection === null){
    connection = {
      id:"",
      connectionName: "", 
      password:"",
      description: "",
      dbName: "",
      host: "",
      dbType: ""
    }
  }
  const [formData, setFormData] = useState({
    description: connection.description,
    host: connection.host,
    dbName: connection.dbName,
    dbType: connection.dbType,
    connectionName: connection.connectionName,
    password: "change_me"
  });

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
                <label htmlFor="dbName" className="form-label d-block text-start">DB Name</label>
                <input type="text" className="form-control" onChange={handleChange} id="dbName" value={formData.dbName} />
              </div>
              <div className="mb-3">
                <label htmlFor="host" className="form-label d-block text-start">Host</label>
                <input type="text" className="form-control" onChange={handleChange} id="host" value={formData.host} />
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">Password</label>
                <input type="password" className="form-control" onChange={handleChange} id="dbType" value={formData.password} />
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
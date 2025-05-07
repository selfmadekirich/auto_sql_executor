import React, { useState, useEffect } from 'react';
import api from '../api';
import { fetchServices, fetchModels  } from '../api/Profiles';




function EditProfileRecordModal({profile, onClose, onSave }){
 
  if (!profile){
    profile = {
      profile_name:"",
      auth_token: "", 
      description: "",
      service: "",
      model_name: "",
      id: ""
    }
  }
  const [formData, setFormData] = useState({
    profile_name: profile.profile_name,
    auth_token: "",
    description: profile.description,
    service: profile.service,
    model_name: profile.model_name,
    id: profile.id
  });


  const [services, setServices] = useState([]);
  const [models, setModels] = useState([]);
 
  useEffect(() => {
    fetchServices(setServices, 
      (error) => {console.error('Error fetching data:', error)})
    
    if (profile.service){
      fetchModels(profile.service,
        setModels,
       (error) => {console.error('Error fetching data:', error)})
    }
  }, []);


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });

    if(e.target.id === "service"){
      
        fetchModels(e.target.value,
           setModels,
          (error) => {console.error('Error fetching data:', error)})
      
    }
  };

  const handleSubmit = () => {
    const updatedprofile = {
      ...profile,
      ...formData,
    };
    onSave(updatedprofile);
  };

  return (
    <div className="modal" style={{ display: 'block' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Edit AI Profile</h5>
          </div>
          <div className="modal-body">
            <form>
              <div className="mb-3">
                <label htmlFor="profileName" className="form-label d-block text-start">AI profile Name</label>
                <input type="text" className="form-control" onChange={handleChange}  id="profile_name" value={formData.profile_name} />
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">Services</label>
                <select className="form-select" id="service" onChange={handleChange} value={formData.service}>
                  <option value="">Select Service</option>
                  {services.map((type, index) => (
                    <option key={index} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">Models</label>
                <select className="form-select" id="model_name" onChange={handleChange} value={formData.model_name}>
                  <option value="">Select Models</option>
                  {models.map((type, index) => (
                    <option key={index} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label htmlFor="dbType" className="form-label d-block text-start">Auth token</label>
                <input type="password" className="form-control" onChange={handleChange} id="auth_token" value={formData.auth_token} />
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

export default EditProfileRecordModal
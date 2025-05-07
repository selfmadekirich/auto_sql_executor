import React, {useState, useEffect } from 'react';
import ProfileRecord from '../components/ProfileRecord';
import EditProfileRecordModal from '../components/EditProfileRecordModal';
import ProfileDTO from '../dto/Profiles'
import fetchProfiles, { deleteProfile, createProfile, updateProfile } from '../api/Profiles';
import { Notifications } from "react-push-notification";
import { successNotification, errorNotification } from '../utils';

function Profiles() {
     

    const [selectedProfile, setSelectedProfile] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isNewProfileModalOpen, setIsNewProfileModalOpen] = useState(false);

    const [Profiles, setProfiles] = useState([])

    useEffect( () => {
       fetchProfiles(
        setProfiles, (error) => {errorNotification(error.message)});
    }, []);


    const handleEdit = async (profile) => {
        setSelectedProfile(profile);
        setIsModalOpen(true);
    };
    
      const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleNewProfileCloseModal = () => {
        setIsNewProfileModalOpen(false);
    };

    const handleDelete = async (id) => {
        await deleteProfile(id,
          () => {successNotification("","Profile deleted!")},
          (error) => errorNotification(error.message)
        )
        await fetchProfiles(setProfiles, 
          (error) => {errorNotification(error.message)})
    };

      const handleSaveChanges = async (updatedProfile) => {
        
        const dto = new ProfileDTO(updatedProfile);
        await updateProfile(
          dto.id,
          dto.toUpdateProfileAPI(),
          () => {successNotification("","Profile updated!")},
          (error) => errorNotification(error.message)
        )
          
        await fetchProfiles(setProfiles, 
          (error) => {errorNotification(error.message)})
  
        setIsModalOpen(false);
    };


    const handleSaveNewProfile = async (newProfile) => {
      console.log("eeeee")
      console.log(newProfile)
        await createProfile(
          new ProfileDTO(newProfile).toCreateProfileAPI(),
          () => {successNotification("", "Profile added!")},
          (error) => errorNotification(error.message)
        )
          
        await fetchProfiles(setProfiles, 
          (error) => {errorNotification(error.message)})
  
        setIsNewProfileModalOpen(false);
    };


  return (
    <div className="container mt-5">
        <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mt-3">Profiles</h2>
        </div>
        <div className='d-flex justify-content-end mb-4'>
        <button className="btn btn-primary" onClick={() => setIsNewProfileModalOpen(true)}>Add New</button>
        </div>
    <table className="table">
      <thead>
        <tr>
          <th className="text-start">Profile Name</th>
          <th>Description</th>
          <th>Service</th>
          <th>Model</th>
        </tr>
      </thead>
      <tbody className="my-3">
        {Profiles.map((row, index) =>(
          <ProfileRecord 
            key={index}
            profile_name={row.profile_name} 
            description={row.description} 
            service={row.service} 
            model_name={row.model_name}
            onDelete={ () => {handleDelete(row.Profile_id); console.log("delete is pressed")}}
            onEdit={ () => {handleEdit(row)} }

          />
        ))}
      </tbody>
    </table>
    {isModalOpen && (
        <EditProfileRecordModal
          profile={selectedProfile}
          onClose={handleCloseModal}
          onSave={handleSaveChanges}
        />
      )}
      {isNewProfileModalOpen && (
        <EditProfileRecordModal
          profile={null}
          onClose={handleNewProfileCloseModal}
          onSave={handleSaveNewProfile}
        />
      )}
      <Notifications position='bottom-left'/>
  </div>
  );
};

export default Profiles;
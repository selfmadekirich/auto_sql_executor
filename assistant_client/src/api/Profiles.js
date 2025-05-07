import api from "../api";


const fetchProfiles = async (onSuccess, onFailed) => {
    try {
      const response = await api.get('/profiles', {
        params: {
          option: 'All'
        }
      });

      const recoded_data = []
      response.data.map(
        function(item){
          recoded_data.push({
            profile_name: item.profile_name,
            description: item.description,
            service: item.service,
            Profile_id: item.id,
            model_name: item.model_name,
            auth_token: item.auth_token
          })
        }
      )
      onSuccess(recoded_data);
    } catch (error) {
      onFailed(error);
    }
  };


  const fetchProfilesPartial = async (onSuccess, onFailed) => {
    try {
      const response = await api.get('/profiles', {
        params: {
          option: 'Partial'
        }
      });

      const recoded_data = []
      response.data.map(
        function(item){
          recoded_data.push({
            profile_name: item.profile_name,
            Profile_id: item.id
          })
        }
      )
      onSuccess(recoded_data);
    } catch (error) {
      onFailed(error);
    }
  };




  const fetchServices = async (onSuccess, onFailed) => {
    try {
        const response = await api.get('/profiles/references/services');
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const fetchModels = async (service, onSuccess, onFailed) => {
    try {
        const response = await api.get('/profiles/references/services/' + service + '/models');
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const deleteProfile = async (profileId, onSuccess, onFailed) => {
    try {
        const response = await api.delete('/profiles/' + profileId);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const createProfile = async (profile, onSuccess, onFailed) => {
    try {
        const response =await api.post('/profiles',
          profile);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const updateProfile = async (profileId,profileData, onSuccess, onFailed) => {
    try {
        const response =await api.patch('/profiles/' + profileId,
          profileData);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


export default fetchProfiles;
export { fetchServices,fetchModels , deleteProfile, createProfile, updateProfile, fetchProfilesPartial }
import api from "../api";

const computeResults = async (connectionId, userRequest, profile_id ,onSuccess, onFailed) => {
    try {
      const response = await api.post(`/generate/${connectionId}/results`, {
        "user_query": userRequest,
        "profile_id": profile_id
      });
      
      console.log("WHAT A FUCK")
      onSuccess(response.data.result);
    } catch (error) {
        console.log(error)
        onFailed(error);
        console.log("Error here")
    }
  };

export {computeResults}
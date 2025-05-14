import api from "../api";

const computeResults = async (connectionId, userRequest, profile_id ,onSuccess, onFailed) => {
    try {
      const response = await api.post(`/generate/${connectionId}/results`, {
        "user_query": userRequest,
        "profile_id": profile_id
      });
      
      onSuccess(response.data);
    } catch (error) {
        console.log(error)
        onFailed(error);
        console.log("Error here")
    }
  };


  const LoadMoreResults = async (connectionId, sqlQuery, page ,onSuccess, onFailed) => {
    try {
      const response = await api.post(`/generate/${connectionId}/results/load`, {
        "sql_query": sqlQuery,
        "page": page,
        "size": 10
      });
      
      onSuccess(response.data);
    } catch (error) {
        console.log(error)
        onFailed(error);
        console.log("Error here")
    }
  };

export {computeResults, LoadMoreResults }
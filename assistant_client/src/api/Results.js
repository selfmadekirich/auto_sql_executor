import api from "../api";

const computeResults = async (connectionId, userRequest ,onSuccess, onFailed) => {
    try {
      const response = await api.post(`/generate/${connectionId}/results`, {
        "user_query": userRequest
      });

      onSuccess(response.data.result);
    } catch (error) {
        onFailed(error);
    }
  };

export {computeResults}
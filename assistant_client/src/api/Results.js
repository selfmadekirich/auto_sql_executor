import api from "../api";

const computeResults = async (connectionId, userRequest ,onSuccess, onFailed) => {
    try {
      const response = await api.post(`/generate/${connectionId}/results`, {
        "user_query": userRequest
      });

      const recoded_data = []
      console.log(response.data);
      response.data.results.map(
        function(item){
          recoded_data.push({
           item
          })
        }
      )
      onSuccess(recoded_data);
    } catch (error) {
        onFailed(error);
    }
  };

export {computeResults}
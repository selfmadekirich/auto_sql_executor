import api from "../api";


const fetchProjects = async (onSuccess, onFailed) => {
    try {
      const response = await api.get('/db_connections', {
        params: {
          option: 'Partial'
        }
      });

      const recoded_data = []
      response.data.map(
        function(item){
          recoded_data.push({
            connectionName: item.json_props.name,
            description: item.json_props.description,
            dbType: item.db_type,
            connection_id: item.id
          })
        }
      )
      onSuccess(recoded_data);
    } catch (error) {
        onFailed(error);
    }
  };

export {fetchProjects}
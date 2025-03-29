import api from "../api";


const fetchConnections = async (onSuccess, onFailed) => {
    try {
      const response = await api.get('/db_connections', {
        params: {
          option: 'All'
        }
      });

      const recoded_data = []
      response.data.map(
        function(item){
          recoded_data.push({
            connectionName: item.json_props.name,
            description: item.json_props.description,
            dbType: item.db_type,
            connection_id: item.id,
            dbName: item.json_props.db_name,
            host: item.json_props.host,
            port: item.json_props.port,
            user: item.json_props.user,
            schema_name: item.json_props.schema_name
          })
        }
      )
      onSuccess(recoded_data);
    } catch (error) {
      onFailed(error);
    }
  };




  const fetchDb_types = async (onSuccess, onFailed) => {
    try {
        const response = await api.get('/database_types');
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const deleteConnection = async (ConnectionId, onSuccess, onFailed) => {
    try {
        const response = await api.delete('/db_connections/' + ConnectionId);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const createConnection = async (connection, onSuccess, onFailed) => {
    try {
        const response =await api.post('/db_connections',
          connection);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


  const updateConnection = async (connectionId,connectionData, onSuccess, onFailed) => {
    try {
        const response =await api.patch('/db_connections/' + connectionId,
          connectionData);
         onSuccess(response.data);
    } catch (error) {
      onFailed(error);
    }
  };


export default fetchConnections;
export { fetchDb_types, deleteConnection, createConnection, updateConnection }
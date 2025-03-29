
function get(obj, key, defaultValue=null) {
    return key in obj ? obj[key] : defaultValue;
  }

class ConnectionDTO{
    constructor(params) {
        this.id = get(params, 'id');
        this.db_type = get(params, 'dbType');
        this.password = get(params, 'password');
        this.host = get(params, 'host');
        this.port = get(params, 'port');
        this.user = get(params, 'user');
        this.db_name = get(params, 'dbName');
        this.schema_name = get(params, 'schema_name');
        this.description = get(params, 'description');
        this.name = get(params, 'connectionName');
    }

    toCreateConnectionAPI(){
        return {
            db_type: this.db_type,
            json_props: {
                host: this.host,
                port: this.port,
                user: this.user,
                password: this.password,
                db_name: this.db_name,
                schema_name: this.schema_name,
                description: this.description,
                name: this.name
            }
        }
    }


    toUpdateConnectionAPI(){
        return {
            db_type: this.db_type,
            json_props: {
                host: this.host,
                port: this.port,
                user: this.user,
                password: this.password,
                db_name: this.db_name,
                schema_name: this.schema_name,
                description: this.description,
                name: this.name
            }
        }
    }
}


export default ConnectionDTO
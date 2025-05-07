
function get(obj, key, defaultValue=null) {
    return key in obj ? obj[key] : defaultValue;
  }

class ProfileDTO{
    constructor(params) {
        this.id = get(params, 'Profile_id');
        this.profile_name = get(params, 'profile_name');
        this.description = get(params, 'description');
        this.service = get(params, 'service');
        this.model_name = get(params, 'model_name');
        this.auth_token = get(params, 'auth_token');
    }

    toCreateProfileAPI(){
        return {
            db_type: this.db_type,
            profile_name: this.profile_name,
            description: this.description,
            service: this.service,
            model_name: this.model_name,
            auth_token: this.auth_token
        }
    }


    toUpdateProfileAPI(){
        return {
            profile_name: this.profile_name,
            description: this.description,
            service: this.service,
            model_name: this.model_name,
            auth_token: this.auth_token
        }
    }
}


export default ProfileDTO
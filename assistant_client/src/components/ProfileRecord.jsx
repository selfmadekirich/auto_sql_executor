import { Link } from "react-router-dom";
import React from 'react';



function ProfileRecord({profile_name, description, service, model_name, onDelete, onEdit}){
    return (
      <tr style={{ marginBottom: '1rem', marginTop: '10rem' }}>
      <td className="text-start">{profile_name}</td>
      <td>{description}</td>
      <td>{service}</td>
      <td>{model_name}</td>
      <td>
        <button className="btn btn-danger me-2" onClick={onDelete}>
          Удалить
        </button>
        <button className="btn btn-primary" onClick={() => onEdit(profile_name)}>
          Редактировать
        </button>
      </td>
    </tr>
    )
}

export default ProfileRecord
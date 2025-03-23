import { Link } from "react-router-dom";
import React from 'react';



function ConnectionRecord({connectionName, description,host, dbName, dbType, onDelete, onEdit}){
    return (
      <tr style={{ marginBottom: '1rem', marginTop: '10rem' }}>
      <td className="text-start">{connectionName}</td>
      <td>{description}</td>
      <td>{host}</td>
      <td>{dbName}</td>
      <td>{dbType}</td>
      <td>
        <button className="btn btn-danger me-2" onClick={onDelete}>
          Удалить
        </button>
        <button className="btn btn-primary" onClick={() => onEdit(connectionName)}>
          Редактировать
        </button>
      </td>
    </tr>
    )
}

export default ConnectionRecord
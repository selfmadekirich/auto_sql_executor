import { Link } from "react-router-dom";
import React from 'react';



function UserProjectRow({connectionId ,connectionName, description, dbType}){
    return (
        <tr style={{ marginBottom: '1rem', marginTop: '10rem' }}>
        <td className="text-start">
        <Link to={`/results/${connectionId}`}>{connectionName}</Link>
        </td>
        <td>{description}</td>
        <td>{dbType}</td>
      </tr>
    )
}

export default UserProjectRow
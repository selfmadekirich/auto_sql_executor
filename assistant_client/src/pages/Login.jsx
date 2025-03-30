import React, { Component, use, useState } from 'react'
import api from '../api'
import {  useNavigate } from 'react-router-dom'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants'
import { Notifications } from "react-push-notification";
import { successNotification, errorNotification } from '../utils';

function Login(){

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState("")
    const navigate = useNavigate()
    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try{
            const grant_type = 'password'
            let config = { headers: { 'Content-Type': 'application/x-www-form-urlencoded'} }
            const res = await api.post("/token", {username, password, grant_type}, config)
            localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
            navigate('/');
        }
        catch(error){
          errorNotification("Неправильные логин/пароль!")
        }
        finally{
            setLoading(false)
        }
    }

    return (
        <div className="auth-wrapper">
        <div className="auth-inner">
        <form onSubmit={handleSubmit}>
        <h3>Login</h3>

        <div className="mb-3">
          <label>Username</label>
          <input
            type="text"
            className="form-control"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div className="d-grid">
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
      </div>
      <Notifications position='bottom-left'/>
      </div>
    )
    }
    
    export default Login

import react, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Navigate,
  Link
} from "react-router-dom";
import {login, useAuth, logout} from '../auth'
import validator from 'validator'

export default function Login() {

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [singUpUsername, setSingUsername] = useState('')
  const [singUpPassword, setSingPassword] = useState('')
  const token = sessionStorage.getItem("token")
  //const [useAuth, authFetch, login, logout] = useAuthProvider();
  const [logged] = useAuth();

  const onSubmitClick = (e) => {
    e.preventDefault()
    console.log("You pressed login")
    let opts = {
      'username': username,
      'password': password
    }
    console.log(opts)
    fetch('/api/login', {
      method: 'post',
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify(opts)
    }).then(r => r.json())
      .then(token => {
        if (token.access_token) {
          login(token.access_token)
          //sessionStorage.setItem("token", token.access_token)
          console.log(token.access_token)
        }
        else {
          console.log("Please type in correct username/password")
        }
      })
  }

  const onSubmitSingUpClick = (e) => {
    e.preventDefault()
    console.log("You pressed singUp")
    let opts = {
      'username': singUpUsername,
      'password': singUpPassword
    }
    console.log(opts)
    fetch('/api/singUp', {
      method: 'post',
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify(opts)
    }).then(r => r.json())
      .then(token => {
        
          console.log(token.access_token)
        
        
      })
  }
  const [emailError, setEmailError] = useState(false)
  const validateEmail = (e) => {
    var email = e.target.value
  
    if (validator.isEmail(email)) {
      setEmailError('Valid Email :)')
    } else {
      setEmailError('Enter valid Email!')
    }
  }

  const handleUsernameChange = (e) => {
    if (validator.isEmail(e.target.value)) {
      setEmailError('Valid Email :)')
      setUsername(e.target.value)
    } else {
      setEmailError('Enter valid Email!')
    }
    setUsername(e.target.value)
  }

  const handlePasswordChange = (e) => {
    setPassword(e.target.value)
  }
  const handleSingUsernameChange = (e) => {
    if (validator.isEmail(e.target.value)) {
      setEmailError('Valid Email :)')
      setUsername(e.target.value)
    } else {
      setEmailError('Enter valid Email!')
    }
    setSingUsername(e.target.value)
  }

  const handleSingPasswordChange = (e) => {
    setSingPassword(e.target.value)
  }

  return (
    <div>
      <h2>Login</h2>
      {!logged? <form action="#">
        <div>
          
          <input type="email" 
            placeholder="Username" 
            onChange={handleUsernameChange}
            value={username} 
          />
          
        <span style={{
          fontWeight: 'bold',
          color: 'red',
        }}>{emailError}</span>
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            onChange={handlePasswordChange}
            value={password}
          />
        </div>
        <button onClick={onSubmitClick} type="submit" disabled={emailError==='Enter valid Email!'}>
          Login Now
        </button>
      </form>
      //:<button onClick={() => logout()}>Logout</button>}
      : <Navigate to ="/logged"/>}
      <form action="#">
      <div>
          
          <input type="email" 
            placeholder="Username" 
            onChange={handleSingUsernameChange}
            value={singUpUsername} 
          /> 
        <span style={{
          fontWeight: 'bold',
          color: 'red',
        }}>{emailError}</span>
        </div>
        <div>
          <input 
            type="password"
            placeholder="Password"
            onChange={handleSingPasswordChange}
            value={singUpPassword}
          />
        </div>
        <button onClick={onSubmitSingUpClick} type="submit" disabled={emailError==='Enter valid Email!'}>
          singUp
        </button>
        </form>
    </div>
  )
}
 /*  const  [data, setData] = useState([{}])

 useEffect(() => {
   fetch("/members").then(
     res => res.json()
   ).then(
     data => {
       setData(data)
       console.log(data)
         
     }
   )
 }, [])

 return (
   <div>
     {(typeof data.members === 'undefined') ? (
       <p>loading...</p>
     ): (
       data.members.map((member, i) => (
         <p key = {i}>{member}</p>
       ))
     )}

   </div>
 )
}
*/

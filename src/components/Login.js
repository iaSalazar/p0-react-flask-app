
import react, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Navigate,
  Link
} from "react-router-dom";
import {login, useAuth, logout} from '../auth'

export default function Login() {

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
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
    fetch('/login', {
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

  const handleUsernameChange = (e) => {
    setUsername(e.target.value)
  }

  const handlePasswordChange = (e) => {
    setPassword(e.target.value)
  }

  return (
    <div>
      <h2>Login</h2>
      {!logged? <form action="#">
        <div>
          <input type="text" 
            placeholder="Username" 
            onChange={handleUsernameChange}
            value={username} 
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            onChange={handlePasswordChange}
            value={password}
          />
        </div>
        <button onClick={onSubmitClick} type="submit">
          Login Now
        </button>
      </form>
      //:<button onClick={() => logout()}>Logout</button>}
      : <Navigate to ="/"/>}
      
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

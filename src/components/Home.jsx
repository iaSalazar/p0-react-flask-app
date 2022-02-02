import React from "react";
import react, { useState, useEffect } from 'react';
import {login, authFetch, useAuth, logout} from "../auth"
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Navigate,
  useNavigate,
  Link,
  useHistory
} from "react-router-dom";
;
function LogedView() {
  
  let navigate = useNavigate();
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const token = sessionStorage.getItem("token")
  //const [useAuth, authFetch, login, logout] = useAuthProvider();
  const [logged] = useAuth();

  const onSubmitClickEvent = (e) => {
    e.preventDefault()
    console.log("You added one event")
    let opts = {
      'name': name,
      'description': description
    }
    console.log(opts)
    authFetch('/events', {
      method: 'put',
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify(opts)
    }).then(r => r.json())
      .then(r => {
          
          console.log(r)
        
      })
  }
  const handleNameEvent = (e) => {
    setName(e.target.value)
  }

  const handleDescriptionEvent = (e) => {
    setDescription(e.target.value)
  }

 
  return (<div>
    <form action="#">
    <div>
          <input type="text" 
            placeholder="Name"
            onChange={handleNameEvent} 
            value={name}
            //onChange={handleDescription}
            //value={username} 
          />
        </div>
        <div>
          <input
            type="text"
            placeholder="Description"
            onChange={handleDescriptionEvent}
            value={description}
            //onChange={handlePasswordChange}
            //value={password}
          />
        </div>
        <button onClick={onSubmitClickEvent} type="submit">Add event</button>
    </form>
    <button onClick={() => {logout();navigate('login')}  }>Logout</button>
  </div>)
}


function Home() {
  const [message, setMessage] = useState('')
  const [logged] = useAuth()
  let navigate = useNavigate();
  
  useEffect(() => {
    authFetch("/members").then(response => {
      if (response.status === 401){
        setMessage("Sorry you aren't authorized!")
        return null
      }
      return response.json()
    }).then(response => {
      if (response && response.message){
        setMessage(response.message)
      }
    })
  }, [])
  return (
    <div>
    {!logged? 
    <h2>Secret: {message}</h2>
    
    :<div>
      <h2>Secret: {message}</h2>
      <h3>Create an event </h3>
      <LogedView/>
      
      </div>}
    
    </div>
    
  )
}
// function Home() {
//   const [data, setData] = useState([{}])

//   useEffect(() => {
//     authFetch("/members").then(
//       response => {
//         if (response.status === 401){
//           setData("Sorry you aren't authorized!")
//           return null
//         }
//         return response.json()
//     }).then(response => {
//       if (response && response.data){
//         setData(response.data)
//       }
//     })
//   }, [])


//   return (
//     <div className="home">
//       <div class="container">
//         <div class="row align-items-center my-5">
//           <div class="col-lg-7">
//             <img
//               class="img-fluid rounded mb-4 mb-lg-0"
//               src="http://placehold.it/900x400"
//               alt=""
//             />
//           </div>
//           <div class="col-lg-5">
//             <h1 class="font-weight-light">Home</h1>
//             <div>
//               {(typeof data.members === 'undefined') ? (
//                 <p>loading...</p>
//               ) : (
//                 data.members.map((member, i) => (
//                   <p key={i}>{member}</p>
//                 ))
//               )}

//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

export default Home;
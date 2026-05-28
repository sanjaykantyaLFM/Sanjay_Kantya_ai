import ProfileCard from "./components/ProfileCard";


function App(){

  const users = [  //it is array  // it store multiple user one at a time so we can print data of multiple user through map below of it
    {
      id:1,
      name: "Sanjay", 
      role: "Ai intern",
      learning: "Learning react"
    },

    {
      id: 2,
      name: "Kantya",
      role: "Innocent me",
      learning : "Agentix ai"
    },

    {
      id: 3,
      name: "Quintyep",
      role: "Service provider",
      learning: " markering"
    }
  ];

  return (
    <div className="container">
      {
        users.map((user) =>(    // we use map here to print each user data through map()  in users.map here users is above varbile or const that i create and user is for like i to track every users in []
          <ProfileCard
            key = {user.id}  // must be unique all time  
            name = {user.name}  // props.name is prosp passing we passed the data dynamicly 
            role = {user.role}
            learning = {user.learning}
          />
        ))
      }
    </div>
  )
}







// This manually single time print of Profile card but what we do if want to print 100 card then we use *** imp concept map() ** 

// function App(){
//   const name = "sanjay";

//   return (
//     <div>
//       <ProfileCard
//        name="Sanjay"
//        role = "Ai intern"
//        learning = "Learning react broooo" 
//        />
//     </div>
//   );
// }

export default App;
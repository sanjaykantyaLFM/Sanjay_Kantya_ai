import "./ProfileCard.css";


function ProfileCard(props){
    return (
        
        <div className="card">     {/* we create className for css and card css we give in prfilecard.css file*/} {/* This syntax for comment in jsx file */}

        {/* // Now adding image tag */}
            <img
                src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="profile"
            />

            <h2>{props.name}</h2>   {/* taking dynamic input used of // props.name*/}
            <p>{props.role}</p>
            <p>{props.learing}</p>

            {/*adding button */} 
            <button>View Profile    </button> 
        </div>
    );
}

export default ProfileCard;
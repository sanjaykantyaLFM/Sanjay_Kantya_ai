import React from 'react';

const Card = ({ title, body }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{body}</p>
    </div>
  );
}

export default Card;

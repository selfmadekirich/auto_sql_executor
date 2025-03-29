import React , { useState } from 'react';
import { Alert, Button  } from 'react-bootstrap';

function MessageDisplay({ messages  }) {

   const [newmessages, setNewmessages] = useState([]);
  
   /*
   if(initialMessages !== undefined){
   setMessages(initialMessages)
   }
   */
  
  const handleClose = (index) => {
    setNewmessages(messages)
    setNewmessages(messages.filter((_, i) => i !== index));
  };


  return (
    <div style={{ position: 'fixed', bottom: '10px', left: '10px', zIndex: 1000 }}>
      {messages.map((message, index) => (
        <Alert key={index} variant={message.type} onClose={() => handleClose(index)} dismissible>
          {message.text}
        </Alert>
      ))}
    </div>
  );
}

export default MessageDisplay;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

    // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
   
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
     
      // ... do something else with emails ...
      
      
           
      emails.forEach(email => {
        const element = document.createElement('div');
        element.id = "email"
        element.innerHTML = `From - ${email.sender}, Subject - ${email.subject}  -  ${email.timestamp}`;
        
        let bg = "white" 
        if (email.read === true){
          bg = "lightgrey"
          element.style.backgroundColor = bg;
        }
        element.addEventListener('click', () => open_email(email.id, mailbox));
        element.addEventListener('mouseover', function() {element.style.backgroundColor = "green", element.style.color = "white"});
        element.addEventListener('mouseout', function() {
          element.style.backgroundColor = bg, 
          element.style.color = "blue"});
        document.querySelector('#emails-view').append(element);
      });
  });
}
// Send composed email
function send_email() {
  event.preventDefault();
  let email  = {recipients: document.querySelector('#compose-recipients').value,
  subject: document.querySelector('#compose-subject').value,
  body: document.querySelector('#compose-body').value
  }
  console.log(email)
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify(email)
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })
  .then(() => load_mailbox('sent'))
  
}

// Open email
function open_email(id, mailbox) {
  
  // Show read view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';
  
  //retrieve email from id
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email.archived)
    // switch archived flag button
    const btn_archive = document.createElement('button');
    btn_archive.className = "btn btn-sm btn-outline-primary";
    btn_archive.innerHTML = email.archived ? "Unarchive":"Archive"; 
    btn_archive.id = "archive";
    btn_archive.addEventListener('click', function() {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
          })
        }) 
        .then(() => {load_mailbox("inbox")})
    });
    // reply button 
    const btn_reply = document.createElement('button');
    btn_reply.className = "btn btn-sm btn-outline-primary";
    btn_reply.innerHTML = "Reply";
    btn_reply.id="reply";
    btn_reply.addEventListener('click', function(){
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#read-view').style.display = 'none';

      document.querySelector('#compose-recipients').value = `${email.sender}`;
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `\n\n On ${email.timestamp} ${email.sender} wrote: \n ${email.body}`;
    
    })
    //display email
        document.querySelector('#read-view').innerHTML =`
    <ul class="list-group">
      <li class="list-group-item"><strong>From - </strong>${email.sender}</li>
      <li class="list-group-item"><strong>To - </strong>${email.recipients} </li>
      <li class="list-group-item"><strong>Date - </strong>${email.timestamp}</li>
      <li class="list-group-item"><strong>Subject - </strong>${email.subject}</li>
      <li class="list-group-item"><strong>Body - </strong>${email.body}</li>
     </ul> 
      `
      if (mailbox != "sent"){
      document.querySelector('#read-view').append(btn_archive);
      document.querySelector('#read-view').append(btn_reply);
    }
  //mark email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
   
});

  
}




document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function send() {
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    event.preventDefault();
  })
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  load_mailbox('sent');
}

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if (email.sender !== undefined) {
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.substring(0, 3) === "Re:") {
      document.querySelector('#compose-subject').value = email.subject;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = (`On ${email.timestamp}, ${email.sender} wrote: ${email.body}`);
  }
  document.querySelector('#send').addEventListener('click', send);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view-title').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Clear any emails that were shown in previous view
  document.querySelector('#mails').innerHTML = "";
  
  // Fetch emails from API 
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
        // console.log(emails);
        emails.forEach(emails => {
          const mail_item = document.createElement('div');
          mail_item.addEventListener('click', () => {
            view_email(emails.id)
          });
          mail_item.className = 'mail_item';
          mail_item.id = emails.id;
          if (emails.read == false) {
            mail_item.style.background = 'white';
          } else {
            mail_item.style.background = 'lightgrey';
          }
          if (mailbox === 'inbox' || mailbox === 'archive') {
          mail_item.innerHTML = `<div class="container">
            <div class="row">
            <div class="col-3 mail-list-addr trunc">From: ${emails.sender}</div>
            <div class="col trunc">${emails.subject}</div>
            <div class="col mail-list-date">${emails.timestamp}</div>
            </div>
            </div>`;
          }
          if (mailbox === 'sent') {
            mail_item.innerHTML = `<div class="container">
            <div class="row">
            <div class="col-3 mail-list-addr trunc">To: ${emails.recipients}</div>
            <div class="col trunc">${emails.subject}</div>
            <div class="col mail-list-date">${emails.timestamp}</div>
            </div>
            </div>`;
          }
          document.querySelector('#mails').append(mail_item);
        })

    })
};
function view_email(id) { 
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  console.log(document.querySelector('#emails-view-title').innerHTML);
  if (document.querySelector('#emails-view-title').innerHTML == '<h3>Sent</h3>') {
    document.querySelector('#archive').style.display = 'none';
    document.querySelector('#unread').style.display = 'none';
  }
  else {
    document.querySelector('#archive').style.display = 'inline-block';
    document.querySelector('#unread').style.display = 'inline-block';
  }
  if (document.querySelector('#emails-view-title').innerHTML == '<h3>Archive</h3>') {
    document.querySelector('#archive').value = "Unarchive Message";
  } else {
    document.querySelector('#archive').value = "Archive Message";
  }
  read(id);
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // ... do something else with email ...
        document.querySelector('#email-view-from').innerHTML = email.sender;
        document.querySelector('#email-view-to').innerHTML = email.recipients;
        document.querySelector('#email-view-subject').innerHTML = email.subject;
        document.querySelector('#email-view-timestamp').innerHTML = email.timestamp;
        document.querySelector('#email-view-body').innerHTML = email.body;
        document.querySelector('#reply').addEventListener('click', () => compose_email(email));
        document.querySelector('#unread').onclick = () => readUnread(id);
        document.querySelector('#archive').onclick = () => arcUnarc(id);
        });
};

function readUnread(id) {
  if (document.querySelector('#unread').value == 'Mark As Read') {
    document.querySelector('#unread').value = 'Mark As Unread';
    console.log(`ID: ${id}`);
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    .then(response => response.text())
    .then(result => {
        // Print result
        console.log(result);
    });
  } else { 
    document.querySelector('#unread').value = 'Mark As Read';
    console.log(`ID: ${id}`);
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: false
      })
    })
    .then(response => response.text())
    .then(result => {
        // Print result
        console.log(result);
    });
  }
  setTimeout(() => { load_mailbox('inbox')}, 800);
};

function read(id) {
  document.querySelector('#unread').value = 'Mark As Unread';
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  .then(response => response.text())
  .then(result => {
      // Print result
      console.log(result);
  });
};

function archive(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: false
    })
  })
  .then(response => response.text())
  .then(result => {
      // Print result
      console.log(result);
  });
};

function arcUnarc(id) {
  if (document.querySelector('#archive').value == 'Archive Message') {
    document.querySelector('#archive').value = 'Unarchive Message';
    console.log(`ID: ${id}`);
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    .then(response => response.text())
    .then(result => {
        // Print result
        console.log('Archive status updated.');
    });
  } else { 
    document.querySelector('#archive').value = 'Archive Message';
    console.log(`ID: ${id}`);
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(response => response.text())
    .then(result => {
        // Print result
        console.log('Archive status updated.');
    });
  }
  setTimeout(() => { load_mailbox('inbox')}, 500);
};
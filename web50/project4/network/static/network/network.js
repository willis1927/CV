
function edit_post(id, text) {

    document.getElementById(`${id}_h6`).innerHTML = `<textarea cols = "75" rows="5" id = "${id}_text">${text}</textarea>`;
    document.getElementById(`${id}_edit`).setAttribute("hidden",true);
    document.getElementById(`${id}_submit`).removeAttribute("hidden");  
      
}

function submit_edit(id, text){
   
  let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
 
  fetch(`/edit/${id}`, {
    method: 'POST',
    headers: {
        'Content-type':"application/json",
        'X-CSRFToken': csrfToken,
      },
    body: JSON.stringify({
        text: text})
  })
    .then(response => response.json())
  .then(result => {
   
    document.getElementById(`${id}_h6`).innerHTML =`${result.text}`;
    document.getElementById(`${id}_edit`).removeAttribute("hidden");
    document.getElementById(`${id}_submit`).setAttribute("hidden",true);
})
  
}

function updateLikes(id, liked){
count = document.getElementById(`${id}_likes`).innerHTML

  console.log(count)    
    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    fetch(`/likes`, {
        method: 'POST',
        headers: {
            'Content-type':"application/json",
            'X-CSRFToken': csrfToken,
          },
        body: JSON.stringify({
            id: id,
            liked :liked})
      })
        .then(response => response.json())
        .then(result => {
        //Print result
        console.log(result.message);
        if (liked === 'true') {
            console.log(count)  
            count = parseInt(count) - 1;
            console.log(count)  
            document.getElementById(`${id}_likes`).innerHTML = `${count}`;
            document.getElementById(`${id}_like`).removeAttribute("hidden");
            document.getElementById(`${id}_unlike`).setAttribute("hidden",true);
          } else {
            console.log(count)
            count = parseInt(count) + 1;
            console.log(count)  
            document.getElementById(`${id}_likes`).innerHTML = `${count}`;
            document.getElementById(`${id}_unlike`).removeAttribute("hidden");
            document.getElementById(`${id}_like`).setAttribute("hidden",true);
            
        }
        
        ;
    })
}



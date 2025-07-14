

/*Function to validate phone number input
function phonevalidate(inputtxt)
{ 
  var phoneno = /^[+]\d{12}$/;
  if(inputtxt.value.match(phoneno))
     {
        
      return true;
        }
      else
        {
        alert("Invalid phone number, format - +country code 12 digit phone number omitting first 0");
          
        return false;
      }
}*/

function toggle() {
  var x = document.getElementById("nav-container");
 
  if (x.className === "nav-container") {
    x.className += " responsive";
   
  } else {
    x.className = "nav-container";
    
  }
}

function updateImage(){
  var url = document.getElementById("picture").value;
  if (url != "") { 
  document.getElementById("campsite_img").src=url;
  }
}



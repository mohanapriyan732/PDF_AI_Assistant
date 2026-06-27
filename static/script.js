async function askQuestion(){


let input=document.getElementById("question");

let question=input.value;


if(question.trim()=="") return;



let messages=document.getElementById("messages");



messages.innerHTML +=

`
<div class="message user">
${question}
</div>
`;



input.value="";



messages.innerHTML +=

`
<div class="message bot" id="loading">
Thinking...
</div>
`;



let response = await fetch("/ask",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

question:question

})

});



let data=await response.json();



document.getElementById("loading").remove();



messages.innerHTML +=

`
<div class="message bot">
${data.answer}
</div>
`;



messages.scrollTop=messages.scrollHeight;


}
function toggleChat(){

let chat = document.getElementById("chatbox");

if(chat.style.display === "none" || chat.style.display === ""){
chat.style.display = "block";
}
else{
chat.style.display = "none";
}

}
function handleKey(event){

if(event.key === "Enter"){

let inputBox = document.getElementById("userinput");
let input = inputBox.value.toLowerCase().trim();

if(input === "") return;

let reply = "";

// greetings
if(input.includes("hi") || input.includes("hello")){
reply = "Hello 👋 Welcome to Ramesh Kitchen Mixer. How can I help you?";
}

else if(input.includes("price")){
reply = "Our mixer price starts from ₹4500.";
}

else if(input.includes("order") || input.includes("buy")){
reply = "You can order a mixer from the Products page.";
}

else if(input.includes("repair")){
reply = "Yes, we provide mixer repair service. Please use the Book Repair page.";
}

else if(input.includes("warranty")){
reply = "Our mixers come with 24 months warranty.";
}

else if(input.includes("address") || input.includes("location")){
reply = "Our shop is at Belhe, Tal: Junnar, Dist: Pune.";
}

// thank you
else if(input.includes("thank")){
reply = "You're welcome 😊 Happy to help!";
}

// bye
else if(input.includes("bye")){
reply = "Goodbye 👋 Have a nice day! Visit us again.";
}

// contact
else if(input.includes("contact") || input.includes("phone")){
reply = "You can contact us through the Contact page.";
}

else{
reply = "You can ask about price, order, repair, warranty or address.";
}

let chat = document.getElementById("chatmessages");

chat.innerHTML += "<p><b>You:</b> "+input+"</p>";
chat.innerHTML += "<p><b>AI:</b> "+reply+"</p>";

chat.scrollTop = chat.scrollHeight;

inputBox.value = "";

}

}

// Services page scroll animations
document.addEventListener('DOMContentLoaded', function() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Animate feature and service cards on services page
  document.querySelectorAll('.feature-card, .service-card').forEach(card => {
    if (card) {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      card.style.transition = 'opacity 0.6s, transform 0.6s';
      observer.observe(card);
    }
  });
});
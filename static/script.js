function toggleChat() {
    let chat = document.getElementById("chatbox");
    if (chat.style.display === "none" || chat.style.display === "") {
        chat.style.display = "block";
    } else {
        chat.style.display = "none";
    }
}

function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    let inputBox = document.getElementById("userinput");
    let rawInput = inputBox.value;
    let input = rawInput.toLowerCase().trim();

    if (input === "") return;

    appendMessage("You", rawInput);
    inputBox.value = "";

    setTimeout(() => {
        let reply = generateAIResponse(input);
        appendMessage("🤖 AI", reply);
    }, 400); // Small delay feels more realistic
}

function appendMessage(sender, text) {
    let chat = document.getElementById("chatmessages");
    let isUser = sender === "You";

    // Clean UI for Chat Bubbles
    let align = isUser ? "text-align: right;" : "text-align: left;";
    let color = isUser ? "background-color: #007bff; color: white;" : "background-color: #f1f1f1; color: black;";

    chat.innerHTML += `
        <div style="margin-bottom: 15px; ${align}">
            <div style="display: inline-block; padding: 10px 14px; border-radius: 15px; max-width: 85%; ${color} text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.1); line-height: 1.5;">
                <span style="font-size: 0.8em; opacity: 0.8; display: block; margin-bottom: 3px;">${sender}</span>
                ${text}
            </div>
        </div>
    `;

    // Auto Scroll to bottom
    chat.scrollTop = chat.scrollHeight;
}

function generateAIResponse(input) {
    // 1. Greeting System
    if (input === "hi" || input === "hello" || input === "hey") {
        return "Hello there! 👋 I am your AI Assistant. I can help you with:<br>• 💰 <b>Price</b> / Cost<br>• 🛒 <b>Order</b> / Buy<br>• 🔧 <b>Repair</b> / Service<br>• 🛡️ <b>Warranty</b><br>• 📍 <b>Location</b><br><br>What would you like to know?";
    }

    // 2. Smart Responses
    if (input.includes("price") || input.includes("cost")) {
        return "💰 <b>Mixer Pricing:</b><br>Our premium kitchen mixers range from <b>₹3500 to ₹4550</b>.<br>You can see the exact features and pricing on our <a href='/products' style='color:inherit;text-decoration:underline;'>Products page</a>.";
    }

    if (input.includes("order") || input.includes("buy")) {
        return "🛒 <b>How to Order:</b><br>Ordering is easy! Just follow these steps:<br>1️⃣ Go to the <a href='/products' style='color:inherit;text-decoration:underline;'>Products page</a>.<br>2️⃣ Select the mixer you like.<br>3️⃣ Click <b>Order Now (Website)</b> to buy online.<br>4️⃣ Or click <b>Order on WhatsApp</b> to chat directly with us!";
    }

    if (input.includes("repair") || input.includes("service")) {
        return "🔧 <b>Repair Service:</b><br>We provide expert repair services for all kitchen mixers. Please fill out our repair request online by visiting the <a href='/repair' style='color:inherit;text-decoration:underline;'>Book Repair page</a>, and our technician will assist you.";
    }

    if (input.includes("warranty") || input.includes("guarantee")) {
        return "🛡️ <b>Warranty Info:</b><br>Every original Ramesh Kitchen Mixer comes with a solid <b>24-Month Warranty</b> covering all manufacturing defects and motor issues!";
    }

    if (input.includes("location") || input.includes("address")) {
        return "📍 <b>Our Location:</b><br>Our main workshop is located in <b>Belhe, Tal: Junnar, Dist: Pune (Maharashtra 412410)</b>. You can visit us during business hours!";
    }

    if (input.includes("help") || input.includes("support")) {
        return "I am here to help! 🤖 You can ask me about:<br>• Price<br>• How to Order<br>• Repairs<br>• Warranty<br>• Location";
    }

    // 3. Conversation Handling
    if (input.includes("thank you") || input.includes("thanks")) {
        return "You're very welcome! 😊 Let me know if you need anything else.";
    }

    if (input.includes("bye") || input.includes("goodbye")) {
        return "Goodbye! 👋 Thanks for visiting Ramesh Kitchen Mixers. Have a wonderful day!";
    }

    // 4. Error Handling
    return "Sorry, I didn't quite understand that. 🤔<br>Please type a clear keyword like <b>price</b>, <b>order</b>, <b>repair</b>, <b>warranty</b>, or <b>location</b>.";
}

// Services page scroll animations
document.addEventListener('DOMContentLoaded', function () {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
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
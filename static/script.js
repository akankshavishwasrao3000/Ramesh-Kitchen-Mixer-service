// Simple rule-based chatbot for Ramesh Kitchen Mixer
let chatInitialized = false;

function toggleChat() {
    const chatbox = document.getElementById('chatbox');
    const isOpening = chatbox.style.display === 'none' || chatbox.style.display === '';
    
    chatbox.style.display = isOpening ? 'block' : 'none';

    // Show welcome message only the first time the chat is opened
    if (isOpening && !chatInitialized) {
        chatInitialized = true;
        const chatMessages = document.getElementById('chatmessages');
        if (chatMessages && chatMessages.innerHTML.trim() === "") {
            setTimeout(() => {
                const welcomeMsg = `Hello 👋 Welcome to Ramesh Kitchen Mixer!<br><br>I can help you with:<br><br>🛒 Product Information<br>🔧 Mixer Repair Services<br>📦 Delivery Information<br>📍 Shop Location<br>📞 Contact Details<br>💬 WhatsApp Support<br><br>How may I assist you today?`;
                addBotMessage(welcomeMsg);
            }, 300);
        }
    }
}

function handleKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const userInput = document.getElementById('userinput');
    const rawText = userInput.value.trim();
    if (rawText === '') return;

    addUserMessage(rawText);
    userInput.value = '';
    showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator();
        const response = getBotResponse(rawText);
        addBotMessage(response);
    }, 700);
}

function addUserMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble message-user';
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-meta">You · ${getTimeStamp()}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble message-bot';
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-meta">Bot · ${getTimeStamp()}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('d-none');
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('d-none');
    }
}

function getTimeStamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getBotResponse(message) {
    const msg = message.trim().toLowerCase();

    // 1. GIBBERISH DETECTION (The "Worst Case" Warning)
    // Check for random strings like "jsdhfksj" or "aaaaaaa"
    const hasVowels = /[aeiouy]/.test(msg);
    const unusualLength = msg.length > 20 && !msg.includes(' ');
    const repeatedChar = /(.)\1{4,}/.test(msg); // 5+ same chars in a row

    if ((!hasVowels && msg.length > 5) || unusualLength || repeatedChar) {
        return "I'm sorry, I couldn't understand that input. 😅 Please ask a question related to our products, repairs, or orders so I can assist you properly!";
    }

    // 2. DETAILED RESPONSE LOGIC
    let response = "";

    // PRICE & COST
    if (["price", "cost", "amount", "rate", "how much", "mrp", "bucks", "value"].some(k => msg.includes(k))) {
        response += "Our premium mixers range from **₹3500 up to ₹4550**. You can see the specific rates for every model on our Products page.<br><br>";
    }

    // PRODUCT SPECS
    if (["detail", "info", "spec", "feature", "motor", "watt", "jar", "quality", "good"].some(k => msg.includes(k))) {
        response += "Ramesh Mixers are built for durability with **900W motors**, 3 stainless steel jars, and a **24-month warranty**. Each model is designed for high-performance home cooking.<br><br>";
    }

    // REPAIR
    if (["repair", "fix", "service", "working", "problem", "broken", "issue", "mechanic"].some(k => msg.includes(k))) {
        response += "We provide expert repair services for all mixers. Simply fill out the **Repair Request** form on our website, and we will contact you for a pickup or visit.<br><br>";
    }

    // CONTACT & WHATSAPP
    if (["contact", "phone", "mobile", "whatsapp", "call", "number", "reach", "talk"].some(k => msg.includes(k))) {
        response += "You can reach us directly at **+91 9921071945** or click the WhatsApp icon on our site for instant support.<br><br>";
    }

    // LOCATION
    if (["location", "address", "shop", "where", "store", "place", "city", "village", "belhe"].some(k => msg.includes(k))) {
        response += "Ramesh Kitchen Mixer is located in **Belhe, Maharashtra 412410**. You are welcome to visit us during business hours!<br><br>";
    }

    // DELIVERY
    if (["delivery", "shipping", "courier", "send", "receive", "home", "post"].some(k => msg.includes(k))) {
        response += "We offer local delivery. Once you place an order, we'll confirm the delivery timeline (usually 3-7 days) via WhatsApp.<br><br>";
    }

    // ORDERING
    if (["order", "place", "buy", "purchase", "shopping", "cart", "checkout"].some(k => msg.includes(k))) {
        response += "To buy, select your favorite model on the **Products page** and fill the order form. No online payment is needed; we confirm everything on WhatsApp first!<br><br>";
    }

    // 3. IF NO Intent FOUND
    if (response === "") {
        // Handle greetings specifically if no other info requested
        if (["hi", "hello", "hey", "namaste", "morning", "evening"].some(k => msg.includes(k))) {
            return "Hello 👋 Welcome to Ramesh Kitchen Mixer! I can help you with product prices, mixer repairs, delivery details, or our shop location. How may I assist you today?";
        }
        
        if (["thanks", "thank you", "great", "ok", "fine"].some(k => msg.includes(k))) {
            return "You're very welcome! 😊 Let me know if you have any other questions.";
        }

        // Standard Fallback
        return "I can help you with:<br><br>🛒 **Product Pricing** (₹3500 - ₹4550)<br>🔧 **Repair Bookings**<br>📦 **Delivery Information**<br>📍 **Shop Address** (Belhe)<br>📞 **Contact Details**<br><br>Please ask your question or select a topic!";
    }

    return response;
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
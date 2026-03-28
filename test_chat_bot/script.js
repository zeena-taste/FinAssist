// Get DOM elements
const messagesContainer = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');

// Initialize speech recognition (if supported)
let recognition;
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  recognition.onresult = (event) => {
    const transcript = event.results.transcript;
    userInput.value = transcript;
    micBtn.classList.remove('listening');
    sendMessage(); // Auto-send after speech
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    micBtn.classList.remove('listening');
  };

  recognition.onend = () => {
    micBtn.classList.remove('listening');
  };
} else {
  micBtn.disabled = true;
  micBtn.title = "Speech recognition not supported in this browser";
  micBtn.style.opacity = 0.5;
}

// Mock initial messages
const initialMessages = [
  { sender: 'ai', text: 'Good morning, Elias. Your savings trend is up 12% this month. You’re on track to hit your year-end goal early. What can I help you with today?', time: '09:12 AM' },
  { sender: 'user', text: 'Can you show me a breakdown of my discretionary spending last week?', time: '09:14 AM' },
  { sender: 'ai', text: 'Certainly. Last week your discretionary spending totaled $412. Here is the split:', time: '09:15 AM', breakdown: true },
];

// Render initial messages
initialMessages.forEach(msg => addMessage(msg));

// Attach event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

micBtn.addEventListener('click', () => {
  if (!recognition) {
    alert('Speech recognition not supported in this browser.');
    return;
  }

  micBtn.classList.add('listening');
  recognition.start();
});

// Send message function
function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // Add user message
  addMessage({ sender: 'user', text, time: getCurrentTime() });
  userInput.value = '';

  // Define backend URL
  const backendUrl = 'https://finaassist-ai-606038878824.us-central1.run.app/agent/query';

  // Use a fixed user_id for demo
  const payload = {
    user_id: "usr_12345",
    message: text
  };

  fetch(backendUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();
  })
  .then(data => {
    // Extract AI message
    const aiMessage = data.data?.message || "I'm here to help with your finances.";
    const hasBreakdown = data.data?.result?.breakdown || false;

    // Add AI message
    addMessage({
      sender: 'ai',
      text: aiMessage,
      time: getCurrentTime(),
      breakdown: hasBreakdown
    });
  })
  .catch(err => {
    console.error('Error communicating with backend:', err);
    addMessage({
      sender: 'ai',
      text: 'Sorry, I couldn’t reach the server. Try again later or check your connection.',
      time: getCurrentTime()
    });
  });
}

// Add message to chat
function addMessage(msg) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${msg.sender}`;

  const textNode = document.createElement('div');
  textNode.textContent = msg.text;
  msgDiv.appendChild(textNode);

  // If breakdown is true, add the spending categories
  if (msg.breakdown) {
    const breakdownDiv = document.createElement('div');
    breakdownDiv.className = 'breakdown';

    const dining = document.createElement('div');
    dining.className = 'category';
    dining.innerHTML = `<div class="category-title">DINING</div><div class="category-amount">$184</div>`;
    breakdownDiv.appendChild(dining);

    const entertainment = document.createElement('div');
    entertainment.className = 'category';
    entertainment.innerHTML = `<div class="category-title">ENTERTAINMENT</div><div class="category-amount">$128</div>`;
    breakdownDiv.appendChild(entertainment);

    msgDiv.appendChild(breakdownDiv);
  }

  const timeDiv = document.createElement('div');
  timeDiv.className = 'message-time';
  timeDiv.textContent = msg.time;
  msgDiv.appendChild(timeDiv);

  messagesContainer.appendChild(msgDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Get current time
function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
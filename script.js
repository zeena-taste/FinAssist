// ==============================
// 📦 DOM Elements
// ==============================
const el = {
  messages: document.getElementById('chat-messages'),
  input: document.getElementById('user-input'),
  send: document.getElementById('send-btn'),
  mic: document.getElementById('mic-btn')
};

// ==============================
// 🧠 App State
// ==============================
let recognition = null;
let isListening = false;

// ==============================
// 🎤 Speech Recognition
// ==============================
(function initSpeech() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    el.mic.disabled = true;
    el.mic.title = "Speech recognition not supported";
    return;
  }

  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.continuous = false;

  recognition.onstart = () => {
    isListening = true;
    el.mic.classList.add('listening');
  };

  recognition.onend = () => {
    isListening = false;
    el.mic.classList.remove('listening');
  };

  recognition.onerror = (e) => {
    console.error('Speech error:', e.error);
  };

  recognition.onresult = (e) => {
    const transcript = e.results?.[0]?.[0]?.transcript || '';
    if (!transcript) return;

    el.input.value = transcript;
    queueMicrotask(sendMessage); // smoother than setTimeout
  };
})();

// ==============================
// 🎯 Event Listeners
// ==============================
el.send.onclick = sendMessage;

el.input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});

el.mic.onclick = () => {
  if (!recognition) return;

  if (isListening) {
    recognition.stop();
  } else {
    try {
      recognition.start();
    } catch {
      // ignore duplicate start errors
    }
  }
};

// ==============================
// 💬 Messaging Core
// ==============================
async function sendMessage() {
  const text = el.input.value.trim();
  if (!text) return;

  el.input.value = '';

  addMessage({ sender: 'user', text });

  const loadingEl = addMessage({
    sender: 'ai',
    text: 'Thinking...',
    loading: true
  });

  try {
    const data = await fetchWithTimeout(
      'https://finaassist-ai-606038878824.us-central1.run.app/agent/query',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'usr_12345', message: text })
      },
      10000
    );

    removeMessage(loadingEl);

    const msg = data?.data?.message ?? 'Unexpected response.';
    const breakdown = data?.data?.result?.breakdown ?? null;

    addMessage({
      sender: 'ai',
      text: msg,
      breakdown
    });

  } catch (err) {
    console.error(err);
    removeMessage(loadingEl);

    addMessage({
      sender: 'ai',
      text: 'Connection issue. Please try again.'
    });
  }
}

// ==============================
// 🌐 Fetch with Timeout
// ==============================
async function fetchWithTimeout(url, options, timeout = 8000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  const res = await fetch(url, {
    ...options,
    signal: controller.signal
  });

  clearTimeout(id);

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ==============================
// 🧱 UI Helpers
// ==============================
function addMessage({ sender, text, breakdown }) {
  const msg = document.createElement('div');
  msg.className = `message ${sender}`;

  const body = document.createElement('div');
  body.textContent = text;
  msg.appendChild(body);

  // 📊 Breakdown rendering
  if (breakdown && typeof breakdown === 'object') {
    const box = document.createElement('div');
    box.className = 'breakdown';

    for (const [key, val] of Object.entries(breakdown)) {
      const item = document.createElement('div');
      item.className = 'category';

      item.innerHTML = `
        <div class="category-title">${key.toUpperCase()}</div>
        <div class="category-amount">$${val}</div>
      `;

      box.appendChild(item);
    }

    msg.appendChild(box);
  }

  const time = document.createElement('div');
  time.className = 'message-time';
  time.textContent = getTime();
  msg.appendChild(time);

  el.messages.appendChild(msg);
  el.messages.scrollTop = el.messages.scrollHeight;

  return msg;
}

function removeMessage(node) {
  node?.remove();
}

// ==============================
// 🕒 Time
// ==============================
function getTime() {
  return new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
}

// ==============================
// 🧪 Seed Data (Optional)
// ==============================
[
  {
    sender: 'ai',
    text: 'Good morning. Your savings are up 12% this month.'
  },
  {
    sender: 'user',
    text: 'Show my spending breakdown'
  },
  {
    sender: 'ai',
    text: 'Here is your breakdown:',
    breakdown: { dining: 184, entertainment: 128 }
  }
].forEach(addMessage);
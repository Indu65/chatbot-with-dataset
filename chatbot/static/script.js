// static/script.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messages = document.getElementById('messages');

  function addMessage(text, who='bot') {
    const el = document.createElement('div');
    el.className = `message ${who}`;
    // preserve newlines in bot replies
    el.innerHTML = text.split('\n').map(s => `<div>${escapeHtml(s)}</div>`).join('');
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  function escapeHtml(unsafe) {
    return unsafe
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    input.value = '';
    addMessage('Thinking...', 'bot typing');

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      // remove the typing message
      const typing = document.querySelector('.message.typing');
      if (typing) typing.remove();
      addMessage(data.reply || "Sorry, I didn't get that.", 'bot');
    } catch (err) {
      const typing = document.querySelector('.message.typing');
      if (typing) typing.remove();
      addMessage("Error contacting server. Is the backend running?", 'bot');
      console.error(err);
    }
  });
});

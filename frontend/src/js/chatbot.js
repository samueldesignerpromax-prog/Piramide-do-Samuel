function openChatbot() {
  const modal = document.getElementById("chatbot-modal");
  if (modal) {
    modal.style.display = "flex";
  }
}

function closeChatbot() {
  const modal = document.getElementById("chatbot-modal");
  if (modal) {
    modal.style.display = "none";
  }
}

function addMessage(content, sender = "bot") {
  const messages = document.getElementById("chat-messages");
  if (!messages) return;

  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = content;

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("chat-input");
  if (!input) return;

  const mensagem = input.value.trim();
  if (!mensagem) return;

  addMessage(mensagem, "user");
  input.value = "";

  try {
    const resposta = await API.enviarMensagemChatbot(mensagem);
    addMessage(resposta.resposta || "Não consegui responder agora.", "bot");
  } catch (error) {
    console.error(error);
    addMessage(`Erro: ${error.message}`, "bot");
  }
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

window.openChatbot = openChatbot;
window.closeChatbot = closeChatbot;
window.sendMessage = sendMessage;
window.handleKeyPress = handleKeyPress;

window.addEventListener("click", (event) => {
  const modal = document.getElementById("chatbot-modal");
  if (event.target === modal) {
    closeChatbot();
  }
});

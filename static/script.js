const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const uploadCard = document.getElementById("uploadCard");
const fileName = document.getElementById("fileName");

if (browseBtn && fileInput) {
  browseBtn.addEventListener("click", () => fileInput.click());
}

if (fileInput) {
  fileInput.addEventListener("change", () => {
    const file = fileInput.files?.[0];
    fileName.textContent = file ? file.name : "No file selected";
  });
}

if (uploadCard) {
  uploadCard.addEventListener("dragover", (event) => {
    event.preventDefault();
    uploadCard.classList.add("dragover");
  });

  uploadCard.addEventListener("dragleave", () => {
    uploadCard.classList.remove("dragover");
  });

  uploadCard.addEventListener("drop", (event) => {
    event.preventDefault();
    uploadCard.classList.remove("dragover");
    const droppedFile = event.dataTransfer?.files?.[0];
    if (droppedFile) {
      fileName.textContent = droppedFile.name;
    }
  });
}

async function askQuestion() {
  let input = document.getElementById("question");
  let question = input.value;

  if (question.trim() == "") return;

  let messages = document.getElementById("messages");

  messages.innerHTML += `
    <div class="message user animate-fade">
      <div class="message-header">
        <span class="message-avatar">👤</span>
        <span class="message-role">You</span>
      </div>
      <p>${question}</p>
    </div>
  `;

  input.value = "";

  messages.innerHTML += `
    <div class="message bot typing animate-fade" id="loading">
      <div class="message-header">
        <span class="message-avatar">🤖</span>
        <span class="message-role">Assistant</span>
      </div>
      <p>Thinking...</p>
    </div>
  `;

  let response = await fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
    }),
  });

  let data = await response.json();

  document.getElementById("loading").remove();

  messages.innerHTML += `
    <div class="message bot animate-fade">
      <div class="message-header">
        <span class="message-avatar">🤖</span>
        <span class="message-role">Assistant</span>
      </div>
      <p>${data.answer}</p>
    </div>
  `;

  messages.scrollTop = messages.scrollHeight;
}

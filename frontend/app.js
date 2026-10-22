const API_BASE = "http://127.0.0.1:8000";
const input = document.getElementById("urlInput");
const button = document.getElementById("analyzeBtn");
const statusText = document.getElementById("status");
const results = document.getElementById("results");

button.addEventListener("click", analyze);
input.addEventListener("keydown", event => {
  if (event.key === "Enter") analyze();
});

async function analyze() {
  const url = input.value.trim();
  if (!url) {
    statusText.textContent = "Please enter a URL first.";
    input.focus();
    return;
  }
  button.disabled = true;
  statusText.textContent = "Analyzing URL…";
  results.classList.add("hidden");

  try {
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis failed. Is the backend running?");
    showResults(data);
    statusText.textContent = "Analysis complete.";
  } catch (error) {
    statusText.textContent = `${error.message} Start the FastAPI server and try again.`;
  } finally {
    button.disabled = false;
  }
}

function showResults(data) {
  results.classList.remove("hidden");
  document.getElementById("prediction").textContent = data.prediction;
  const badge = document.getElementById("riskBadge");
  badge.textContent = `${data.risk_level} risk`;
  badge.className = `badge ${data.risk_level.toLowerCase()}`;
  document.getElementById("score").textContent = `${data.risk_score}/100`;
  document.getElementById("meterFill").style.width = `${data.risk_score}%`;
  document.getElementById("reasons").replaceChildren();
  data.reasons.forEach(reason => {
    const li = document.createElement("li");
    li.textContent = reason;
    document.getElementById("reasons").appendChild(li);
  });
  document.getElementById("action").textContent = data.response.action.replaceAll("_", " ");
  document.getElementById("responseMessage").textContent = data.response.message;
  document.getElementById("simulated").textContent =
    data.response.simulated ? "Simulation only: no real blocking or reporting was performed." : "";
  document.getElementById("note").textContent = data.note;
}

(() => {
  const $ = (id) => document.getElementById(id);
  const messages = $("messages"), form = $("form"), input = $("question"), send = $("send");

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function addMessage(role, text, sources) {
    const empty = $("empty");
    if (empty) empty.remove();
    const wrap = el("div", "msg " + role);
    wrap.appendChild(el("div", "who", role === "user" ? "You" : "Knowledge Assistant"));
    wrap.appendChild(el("div", "body", text));
    if (sources && sources.length) {
      const d = el("details", "sources");
      d.open = true;
      d.appendChild(el("summary", null, "Sources (" + sources.length + ")"));
      const ol = el("ol");
      sources.forEach((s) => {
        const li = el("li");
        li.appendChild(el("div", "meta",
          s.source + (s.section ? " - " + s.section : "") + " (relevance " + s.score.toFixed(2) + ")"));
        li.appendChild(el("div", "snip", s.snippet));
        ol.appendChild(li);
      });
      d.appendChild(ol);
      wrap.appendChild(d);
    }
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
    return wrap;
  }

  async function ask(question) {
    addMessage("user", question);
    const pending = addMessage("assistant", "Searching company records...");
    send.disabled = true;
    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      pending.remove();
      if (!res.ok) {
        const wrap = addMessage("assistant", data.detail || "Request failed.");
        wrap.classList.add("error");
      } else {
        addMessage("assistant", data.answer, data.sources);
      }
    } catch (err) {
      pending.remove();
      addMessage("assistant", "Could not reach the server. Check that it is running.").classList.add("error");
    } finally {
      send.disabled = false;
      input.focus();
    }
  }

  async function loadHealth() {
    try {
      const h = await (await fetch("/api/health")).json();
      $("st-status").textContent = h.status === "ok" ? "Online" : "Starting";
      $("st-docs").textContent = h.documents;
      $("st-chunks").textContent = h.chunks;
      $("st-model").textContent = h.model;
      $("st-key").textContent = h.llm_configured ? "Configured" : "Missing";
    } catch (e) {
      $("st-status").textContent = "Offline";
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) return;
    input.value = "";
    ask(q);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });
  document.querySelectorAll(".examples .link").forEach((b) =>
    b.addEventListener("click", () => { input.value = b.textContent; input.focus(); }));
  $("reindex").addEventListener("click", async (e) => {
    e.target.disabled = true; e.target.textContent = "Indexing...";
    try { await fetch("/api/ingest", { method: "POST" }); } catch (_) {}
    e.target.disabled = false; e.target.textContent = "Re-index documents";
    loadHealth();
  });

  loadHealth();
  setInterval(loadHealth, 30000);
})();

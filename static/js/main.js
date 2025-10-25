// Minimal client-side helpers for interactive flows
async function postJSON(path, data) {
  const res = await fetch(path, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(data)
  });
  return res.json();
}

async function getJSON(path) {
  const res = await fetch(path);
  return res.json();
}

// Example: add event form handler (if present)
document.addEventListener("DOMContentLoaded", () => {
  const eventForm = document.getElementById("eventForm");
  if (eventForm) {
    eventForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(eventForm);
      const data = Object.fromEntries(fd.entries());
      await postJSON("/api/events", data);
      window.location.reload();
    });
  }

  const noticeForm = document.getElementById("noticeForm");
  if (noticeForm) {
    noticeForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(noticeForm);
      const data = Object.fromEntries(fd.entries());
      await postJSON("/api/notices", data);
      window.location.reload();
    });
  }

  // complaint form
  const compForm = document.getElementById("complaintForm");
  if (compForm) {
    compForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(compForm);
      const data = Object.fromEntries(fd.entries());
      await postJSON("/api/complaints", data);
      window.location.reload();
    });
  }

  // feedback
  const feedbackForm = document.getElementById("feedbackForm");
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(feedbackForm);
      const data = Object.fromEntries(fd.entries());
      await postJSON("/api/feedback", data);
      window.location.reload();
    });
  }

  // attendance short UI
  const attForm = document.getElementById("attendanceForm");
  if (attForm) {
    attForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(attForm);
      const data = Object.fromEntries(fd.entries());
      await postJSON("/api/attendance", data);
      window.location.reload();
    });
  }
});

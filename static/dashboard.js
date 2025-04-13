// JS to handle modal display and form submission

function openAddMemberModal() {
    document.getElementById("addMemberModal").classList.remove("hidden");
    document.getElementById("addMemberModal").classList.add("flex");
  }
  function closeAddMemberModal() {
    document.getElementById("addMemberModal").classList.add("hidden");
    document.getElementById("addMemberModal").classList.remove("flex");
  }
  
  function openAddExpenseModal() {
    document.getElementById("addExpenseModal").classList.remove("hidden");
    document.getElementById("addExpenseModal").classList.add("flex");
  }
  function closeAddExpenseModal() {
    document.getElementById("addExpenseModal").classList.add("hidden");
    document.getElementById("addExpenseModal").classList.remove("flex");
  }

  
  // Add member form submit
  const addMemberForm = document.getElementById("addMemberForm");
  if (addMemberForm) {
    addMemberForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(addMemberForm);
      const payload = Object.fromEntries(formData.entries());
      const response = await fetch("/api/members", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (response.ok) {
        addMemberForm.reset();
        closeAddMemberModal();
        location.reload();
      }
    });
  }
  
  // Add expense form submit
  const addExpenseForm = document.getElementById("addExpenseForm");
  if (addExpenseForm) {
    addExpenseForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(addExpenseForm);
      const payload = Object.fromEntries(formData.entries());
      payload.amount = parseFloat(payload.amount);
      const response = await fetch("/api/expenses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (response.ok) {
        addExpenseForm.reset();
        closeAddExpenseModal();
        location.reload();
      }
    });
  }

  document.getElementById("addMemberForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());
  
    await fetch("/api/members", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  
    this.reset();
    closeAddMemberModal();
    location.reload();
  });


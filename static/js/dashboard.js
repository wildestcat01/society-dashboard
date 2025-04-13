
document.querySelectorAll('.edit-btn').forEach(button => {
  button.addEventListener('click', function () {
    const memberId = this.dataset.memberId;
    fetch(`/get-member/${memberId}`)
      .then(res => res.json())
      .then(member => {
        const form = document.querySelector("#edit-member-form");
        form.id.value = member.id;
        form.full_name.value = member.full_name;
        form.mobile.value = member.mobile;
        form.email.value = member.email;
        form.flat_number.value = member.flat_number;
        form.alternate_phones.value = (member.alternate_phones || []).join(", ");
        form.vehicle_numbers.value = (member.vehicle_numbers || []).join(", ");
        form.ownership_type.value = member.ownership_type || "Owned";
        form.locked.checked = member.home_locked;
        document.getElementById("editMemberModal").style.display = "block";
      });
  });
});

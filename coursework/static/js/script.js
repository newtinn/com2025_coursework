function toggleAddMember() {
    let form = document.getElementById("newMemberForm");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
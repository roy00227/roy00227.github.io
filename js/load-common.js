// js/load-common.js
function loadCommonParts() {
  fetch("/header.html")
    .then(res => res.text())
    .then(data => document.getElementById("header").innerHTML = data);

  fetch("/footer.html")
    .then(res => res.text())
    .then(data => document.getElementById("footer").innerHTML = data);
}

<script>
  document.addEventListener("DOMContentLoaded", loadCommonParts);
</script>
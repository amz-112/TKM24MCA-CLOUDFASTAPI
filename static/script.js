document.addEventListener("DOMContentLoaded", function () {
  fetchItems();
});

document.getElementById("addForm").addEventListener("submit", function (event) {
  event.preventDefault();
  let name = document.getElementById("name").value;
  let description = document.getElementById("description").value;

  fetch("/add", {
      method: "POST",
      body: new URLSearchParams({ "name": name, "description": description }),
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
  }).then(response => response.json())
  .then(data => {
      alert(data.message);
      fetchItems();
  });
});

function fetchItems() {
  fetch("/items")
      .then(response => response.json())
      .then(items => {
          let list = document.getElementById("itemsList");
          list.innerHTML = "";
          items.forEach(item => {
              let li = document.createElement("li");
              li.innerHTML = `${item.name} - ${item.description} 
                              <button onclick="deleteItem(${item.id})">Delete</button>`;
              list.appendChild(li);
          });
      });
}

function deleteItem(id) {
  fetch(`/delete/${id}`, { method: "DELETE" })
      .then(response => response.json())
      .then(data => {
          alert(data.message);
          fetchItems();
      });
}

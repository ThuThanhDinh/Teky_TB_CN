let user = "AnonymousUser"; // Default value
let csrftoken = "";
const csrfElement = document.querySelector("[name=csrfmiddlewaretoken]");
if (csrfElement) {
  csrftoken = csrfElement.getAttribute("value") || "";
}
let btns = document.getElementsByClassName("addtocart");

for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function () {
    let productId = this.dataset.product;

    let action = this.dataset.action;

    location.reload();

    if (typeof user !== "undefined" && user === "AnonymousUser") {
      alert("bạn chưa đăng nhập");
    } else if (typeof user !== "undefined") {
      updateCart(productId, action);
    }
  });
}

function updateCart(id, action) {
  let url = "/updatecart";

  fetch(url, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",

      "X-CSRFToken": csrftoken,
    },

    body: JSON.stringify({ productId: id, action: action }),
  })
    .then((response) => response.json())

    .then((data) => console.log(data));
}

let quantityFields = document.getElementsByClassName("quantity");

for (let i = 0; i < quantityFields.length; i++) {
  quantityFields[i].addEventListener("change", function () {
    let quantityValue = quantityFields[i].getAttribute("value") || "";

    let quantityProduct = "";
    const parentElement = quantityFields[i].parentElement;
    if (
      parentElement &&
      parentElement.parentElement &&
      parentElement.parentElement.children[1] &&
      parentElement.parentElement.children[1].children[0]
    ) {
      const element = parentElement.parentElement.children[1].children[0];
      quantityProduct = element.textContent || "";
    }

    let url = "/updatequantity";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken, 
      },
      body: JSON.stringify({
        qfv: quantityValue,
        qfp: quantityProduct,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        location.reload();
      })
      .catch((error) => {
        console.error("Error updating quantity:", error);
      });
  });
}

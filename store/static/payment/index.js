const { event, error } = require("jquery");

var stripe = Stripe('pk_test_51N5UQkALK2slzOqCrAjtxhSWSxhxbulOFlGRxxYBC5hhVD63CC7PCxTyoCFKMxVi0zXTy8sp1euItgDoFbY0w4tQ00GSoHEWjz')

var elem = document.getElementById("submit");
clientsecret = elem.getAttribute("data-secret");

var elements = stripe.elements();

var style = {
    base: {
        color: "#000",
        lineHeight: 2.4,
        fontSize: "16px",
    }
};

var card = elements.create("card", {style: style});
card.mount("#card-element");

card.on("change", function (eve) {
    var displayError = document.getElementById("card-errors")
    if (event.error) {
        displayError.textContent = event,error.message;
        $("#card-errors").addClass("alert alert-info")
    } else {
        displayError.textContent = "";
        $("card-errors").removeClass("alert alert-info");
    }
});

var form = document.getElementById("payment-form");


form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postCode").value;

    stripe.confirmCardPayment(clientsecret, {
        payment_method: {
            card: card,
            billing_details: {
                address: {
                    line1: custAdd,
                    line2: custAdd2
                },
                name: custName
            },
        }

}).then (function(result) {
    if (result.error) {
        console.log(error)
    } else {
        if (result.paymentIntent.status === 'succeded') {
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/")
        }
    }
});
var form = document.getElementById("payment-form");


form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postcode").value;

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add/",
        data: {
            order_key: "125d326d656d3d943s1dd",
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post"
        },
        success: function (json) {
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
        }
    });

})
            
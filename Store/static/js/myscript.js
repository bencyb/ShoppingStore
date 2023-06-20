$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/plus_cart/",
        data: {
            prod_id: id // Include the 'prod_id' parameter with its value
        },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Log the detailed error response
        }
    });
});



document.querySelectorAll('.minus-cart').forEach(minusButton => {
    minusButton.addEventListener('click', () => {
        const id = minusButton.getAttribute('pid').toString();
        const eml = minusButton.parentNode.children[2];
        
        fetch(`/minus_cart/?prod_id=${id}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            eml.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalamount;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});






$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url: "/remove_cart/",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
        }
    })
})



$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/plus_wishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            // alert(data.message);
            window.location.href = "/product-detail/" + id;
        }
    });
});

$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minus_wishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            window.location.href = "/product-detail/" + id;
        }
    });
});

let cart = []

function addToCart(id,name,price){
    cart.push({id,name,price})
    renderCart()
}

function renderCart(){
    let list=document.getElementById("cart")
    list.innerHTML=""

    let total=0

    cart.forEach(item=>{
        total+=item.price
        list.innerHTML+=`<li>${item.name} - $${item.price}</li>`
    })

    document.getElementById("total").innerText=total
}

function checkout(){
    fetch("/sales/checkout/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCookie("csrftoken")
        },
        body:JSON.stringify({cart:cart})
    }).then(()=>location.reload())
}

function getCookie(name){
    let v=document.cookie.match('(^|;) ?'+name+'=([^;]*)(;|$)')
    return v ? v[2] : null
}

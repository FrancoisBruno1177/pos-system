let barcode = "";

document.addEventListener("keypress", function(e){

if(e.key === "Enter"){

fetch("/api/products/"+barcode)
.then(r=>r.json())
.then(data=>{

addToCart(data)

})

barcode=""

}else{

barcode += e.key

}

})

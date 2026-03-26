let offlineSales=[]

function saveOfflineSale(sale){

offlineSales.push(sale)

localStorage.setItem(

"offlineSales",

JSON.stringify(offlineSales)

)

}

window.addEventListener("online",syncSales)

function syncSales(){

let sales=JSON.parse(

localStorage.getItem("offlineSales")

)

if(!sales)return

sales.forEach(s=>{

fetch("/api/sales/",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify(s)

})

})

localStorage.removeItem("offlineSales")

}

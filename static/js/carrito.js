// Variables
const carrito = document.getElementById('lista-carrito');
const productos = document.getElementsByClassName('products__container');
const highlights = document.getElementsByClassName('highlights__container');
const listaproductos = document.querySelector('#lista-carrito tbody');
const valorTotalDiv = document.getElementsByClassName('modal-total');
const iconBasket = document.getElementsByClassName('icon-basket');
const addCarritoDetail = document.getElementsByClassName('add-carrito');
const BuyCarritoDetail = document.getElementsByClassName('buy-carrito');
const msgCarrito = document.getElementById("msgAdd")
const msgCarritoProductos = document.getElementById("text-car-product")
const divCarritoProductos = document.getElementById("div-card-product")
var valorTotalSuma = 0
// var valorTotalValue = `$ ${valorTotalSuma} COP`
// const vaciarCarritoBtn = document.getElementById('vaciar-carrito');

// Event Listeners
cargarEventListeners();

function cargarEventListeners() {
  displayTotal(valorTotalSuma)
  displayTotalProductos(getValueCantidadProducts())
  
  // Se activa cuando se presiona "Agregar Carrito"
  // productos.addEventListener('click', comprarproducto);
  Array.from(productos).forEach(function(element) {
    element.addEventListener('click', comprarproducto);
  });

  Array.from(highlights).forEach(function(element) {
    element.addEventListener('click', comprarproducto);
  });

  if (addCarritoDetail.length) {
    addCarritoDetail[0].addEventListener('click', comprarproducto);
  }

  // // Cuando se elimina un producto del carrito
  carrito.addEventListener('click', eliminarproducto);

  // // Al vaciar el carrito
  // vaciarCarritoBtn.addEventListener('click', vaciarCarrito);

  // // Al cargar el documento mostrar LS
  document.addEventListener('DOMContentLoaded', leerLocalStorage);
}

function getValueCantidadProducts(){
  productosLS = obtenerproductosLocalStorage();
  cantidad_total = 0
  productosLS.forEach(function(producto) {
        cantidad_total += parseInt(producto.cantidad)
  });
  localStorage.setItem('cantidad_total', cantidad_total );
  return cantidad_total
}

function displayTotal(calculatedValue) {
  valorTotalDiv[0].querySelector('h5').textContent = `$ ${calculatedValue} COP`
}

function displayTotalProductos(cantidad) {
  msgCarritoProductos.innerHTML =  cantidad + " productos en el carrito"
  if(cantidad > 0){
    divCarritoProductos.style.display = "block";
  }
}

function checkIfProductsExist() {
  const products = JSON.parse(localStorage.getItem('productos') )
  if (products && products.length) {
    iconBasket[0].classList.add('add-product');
  } else {
    iconBasket[0].classList.remove('add-product');
  }
}

// Funciones
// Funcion que añade el producto al carrito
function comprarproducto(e) {
  e.preventDefault();
  // Delegation para agregar-carrito
  if(e.target.classList.contains('add-carrito') ) {
    const producto = JSON.parse(e.target.getAttribute('data-product-serialize'));
    const cantidad = document.getElementById('cantidad-' + producto.id + '')
    const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
    producto.especificaciones = ""
    producto.cantidad = 0
    producto.total_precio = producto.costo
    if(especificaciones){
      producto.especificaciones = especificaciones.value
    }
    if (cantidad && cantidad.value){
      producto.cantidad = cantidad.value
      producto.total_precio = producto.total_precio * producto.cantidad
    }
    msgCarrito.style.display = "block";
    
    setTimeout(function() {
        msgCarrito.style.display = "none";         
    },2500);
    // Enviamos el producto seleccionado para obtener sus datos
    leerDatosproducto(producto);
  }
}

// Lee los datos del producto
function leerDatosproducto(producto) {
  const infoProducto = {
    titulo: producto.nombre,
    precio: producto.costo,
    total_precio: producto.total_precio,
    cantidad: producto.cantidad,
    especificaciones: producto.especificaciones,
    id: producto.id
  };

  insertarCarrito(infoProducto);
}

// Muestra el producto seleccionado en el carrito
function insertarCarrito(producto) {
  const row = document.createElement('tr');
  var ifProductExist = checkIfItemExists(producto.id);
  row.innerHTML = `
    <th scope="row">${producto.titulo}</th>
    <td>${producto.cantidad}</td>
    <td>$ ${producto.precio} COP</td>
    <td>$ ${producto.total_precio} COP</td>
    <td class="delete-check">
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value=""
            id="defaultCheck1">
        </div>
        <a style="color:red;" href="#" data-precio-total="${producto.total_precio}" data-cantidad="${producto.cantidad}" data-precio="${producto.precio}" data-id="${producto.id}" class="icon-trash-empty"></a>
    </td>`;
  if (!ifProductExist) {
    listaproductos.appendChild(row);
    valorTotalSuma += parseInt(producto.total_precio)
    displayTotal(valorTotalSuma)

    cantidad_total = localStorage.getItem('cantidad_total') ? localStorage.getItem('cantidad_total') : 0;
    cantidad_total = parseInt(cantidad_total) + parseInt(producto.cantidad)
    localStorage.setItem('cantidad_total', cantidad_total );
    displayTotalProductos(cantidad_total)

    if(divCarritoProductos.style.display == "none"){
      divCarritoProductos.style.display = "block";
    }
  }
  guardarproductoLocalStorage(producto);

 
}

// Elimina el producto del carrito en el DOM
function eliminarproducto(e) {
  e.preventDefault();

  let producto, productoID;
    if(e.target.classList.contains('icon-trash-empty')) {
      e.target.parentElement.parentElement.remove();
      producto = e.target.parentElement.parentElement;
      productoID = producto.querySelector('a').getAttribute('data-id');
    }
    var precioProducto = producto.querySelector('a').getAttribute('data-precio-total')
    valorTotalSuma -= parseInt(precioProducto)

    cantidad_total = parseInt(localStorage.getItem('cantidad_total')) ? localStorage.getItem('cantidad_total') : 0;
    var cantidadProducto = producto.querySelector('a').getAttribute('data-cantidad')
    cantidad_total -= parseInt(cantidadProducto)
    cantidad_total = cantidad_total > 0 ? cantidad_total : 0;
    localStorage.setItem('cantidad_total', cantidad_total );
    displayTotalProductos(cantidad_total)

    if(cantidad_total == 0){
      divCarritoProductos.style.display = "none";
    }

    displayTotal(valorTotalSuma)
    eliminarproductoLocalStorage(parseInt(productoID));

    
}

// Elimina los productos del carrito en el DOM
function vaciarCarrito(e) {
  // Forma lenta con menos codigo
  // listaproductos.innerHTML = '';
  // Forma rapida con mas codigo (recomendada)
  while(listaproductos.firstChild) {
    listaproductos.removeChild(listaproductos.firstChild);
  }

  // Vaciar localStorage
  vaciarLocalStorage();
  displayTotalProductos(0)

  return false;
}

// Almacena productos en el carrito a Local Storage
function guardarproductoLocalStorage(producto) {
  let productos;
  var ifProductExist = checkIfItemExists(producto.id);
  // Toma el valor de un arreglo con datos de LS o vacio
  productos = obtenerproductosLocalStorage();

  if (!ifProductExist) productos.push(producto);

  localStorage.setItem('productos', JSON.stringify(productos) );
  checkIfProductsExist()
}

function checkIfItemExists (id) {
  const items = localStorage.getItem('productos') 
  let itemExists = false
  if (items) {
    const itemsData = JSON.parse(items)
    // check if item with given id exists in local storage data
    itemExists =  itemsData.find(item => item.id === id)
  }

  return itemExists
}

// send to url product
function sendProduct(url){
  productosLS = JSON.parse( localStorage.getItem('productos') );
  if (productosLS && productosLS.length) {
    data = []
    productosLS.forEach(function(producto) {
      data.push({
        "titulo": producto.titulo,
        "cantidad": producto.cantidad,
        "precio": producto.precio,
        "especificaciones": producto.especificaciones,
        "id": producto.id
      })
    })
    location.href=url+'?productos='+JSON.stringify(data)
  }
}

// send to url checkout
function sendCheckout(url, data){
    if (data && data.length) {
      location.href=url+'?productos='+data
    }
}


// send to url checkout direct
function buyProduct(e) {
  e.preventDefault();
  // Delegation para agregar-carrito
  if(e.target.classList.contains('buy-carrito') ) {
    const producto = JSON.parse(e.target.getAttribute('data-product-serialize'));
    const url_checkout = e.target.getAttribute('data-url-checkout');
    const cantidad = document.getElementById('cantidad-' + producto.id + '')
    const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
    producto.especificaciones = ""
    producto.cantidad = 0
    producto.total_precio = producto.costo
    if(especificaciones){
      producto.especificaciones = especificaciones.value
    }
    if (cantidad && cantidad.value){
      producto.cantidad = cantidad.value
      producto.total_precio = producto.total_precio * producto.cantidad
    }
    data = []
    data.push({
      "titulo": producto.descripcion,
      "cantidad": producto.cantidad,
      "precio": producto.costo,
      "especificaciones": producto.especificaciones,
      "id": producto.id
    })
    // Enviamos el producto seleccionado al checkout
    location.href=url_checkout+'?productos='+JSON.stringify(data)
  }
}

// Comprueba que haya elementos en Local Storage
function obtenerproductosLocalStorage() {
  let productosLS;

  // comprobamos si hay algo en localStorage
  if(localStorage.getItem('productos') === null) {
    productosLS = [];
  } else {
    productosLS = JSON.parse( localStorage.getItem('productos') );
  }
  checkIfProductsExist();
  return productosLS;
}

// Imprime los productos de LS en el carrito
function leerLocalStorage() {
  let productosLS;
  checkIfProductsExist()

  productosLS = obtenerproductosLocalStorage();

  productosLS.forEach(function(producto) {
    // Construir el template
    const row = document.createElement('tr');
    row.innerHTML = `
      <th scope="row">${producto.titulo}</th>
      <td>${producto.cantidad}</td>
      <td>$ ${producto.precio} COP</td>
      <td>$ ${producto.total_precio} COP</td>
      <td class="delete-check">
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value=""
              id="defaultCheck1">
          </div>
          <a style="color:red;" href="#" data-precio-total="${producto.total_precio}" data-cantidad="${producto.cantidad}" data-precio="${producto.precio}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
    valorTotalSuma += parseInt(producto.total_precio)
    displayTotal(valorTotalSuma)
    listaproductos.appendChild(row);    
  });
}

// Eliminar el producto por el ID en localStorage
function eliminarproductoLocalStorage(producto) {
  let productosLS;

  // Obtenemos el arreglo de productos
  productosLS = obtenerproductosLocalStorage();

  // Iteramos comparando el ID del producto borrado con los del LS
  productosLS.forEach(function(productoLS, index) {
    if(productoLS.id === producto) {
      productosLS.splice(index, 1);
    }
  });

  // Añadimos el arreglo actual a LS
  localStorage.setItem('productos', JSON.stringify(productosLS) );
  checkIfProductsExist();
}

// Elimina todos los productos de localStorage
function vaciarLocalStorage() {
  localStorage.clear();
}

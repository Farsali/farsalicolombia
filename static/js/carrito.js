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
        cantidad_total += parseInt(producto.cantidad_cajas)
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
    const cantidad_cajas = document.getElementById('cantidad_cajas-' + producto.id + '')
    const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
    producto.especificaciones = ""
    producto.cantidad = 0
    producto.cantidad_cajas = 0
    producto.total_precio = producto.costo
    producto.total_precio_caja = producto.costo_adicional
    if(especificaciones){
      producto.especificaciones = especificaciones.value
    }
    if ((cantidad && cantidad.value > 0) || (cantidad_cajas && cantidad_cajas.value > 0)){

        if (cantidad && cantidad.value > 0){
          producto.cantidad = cantidad.value
          producto.total_precio = producto.total_precio * producto.cantidad
        }

        if (cantidad_cajas && cantidad_cajas.value > 0){
          producto.cantidad_cajas = cantidad_cajas.value
          producto.total_precio_caja = producto.total_precio_caja * producto.cantidad_cajas
        }
        msgCarrito.style.display = "block";
        
        setTimeout(function() {
            msgCarrito.style.display = "none";         
        },2500);
        // Enviamos el producto seleccionado para obtener sus datos
        leerDatosproducto(producto);
    }else{
      alert("Debe ingresar algun valor para insertar en el carrito")
    }
  }
}

// Lee los datos del producto
function leerDatosproducto(producto) {
  const infoProducto = {
    titulo: producto.nombre,
    precio: producto.costo,
    total_precio: producto.total_precio ? producto.total_precio : 0,
    cantidad: producto.cantidad ? producto.cantidad : 0,
    precio_caja: producto.costo_adicional ? producto.costo_adicional : 0,
    total_precio_caja: producto.total_precio_caja ? producto.total_precio_caja : 0,
    cantidad_cajas: producto.cantidad_cajas ? producto.cantidad_cajas : 0,
    especificaciones: producto.especificaciones,
    id: producto.id
  };

  insertarCarrito(infoProducto);
}

// Muestra el producto seleccionado en el carrito
function insertarCarrito(producto) {
  
  var ifProductExist = checkIfItemExists(producto.id);

  if (!ifProductExist) {

    const row = document.createElement('tr');
    if (producto.cantidad && producto.cantidad > 0){
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
          <a style="color:red;" href="#" data-caja="0" data-precio-total="${producto.total_precio}" data-cantidad="${producto.cantidad}" data-precio="${producto.precio}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
      listaproductos.appendChild(row);
    }
    
    const row2 = document.createElement('tr');
    if (producto.cantidad_cajas && producto.cantidad_cajas > 0){
      row2.innerHTML = `
      <th scope="row">${producto.titulo} x Caja</th>
      <td>${producto.cantidad_cajas}</td>
      <td>$ ${producto.precio_caja} COP</td>
      <td>$ ${producto.total_precio_caja} COP</td>
      <td class="delete-check">
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value=""
              id="defaultCheck1">
          </div>
          <a style="color:red;" href="#" data-caja="1" data-precio-total="${producto.total_precio_caja}" data-cantidad="${producto.cantidad_cajas}" data-precio="${producto.precio_caja}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
      listaproductos.appendChild(row2);
    }
      
      valorTotalSuma += parseInt(producto.total_precio)
      valorTotalSuma += parseInt(producto.total_precio_caja)
      displayTotal(valorTotalSuma)

      cantidad_total = localStorage.getItem('cantidad_total') ? localStorage.getItem('cantidad_total') : 0;
      cantidad_total = parseInt(cantidad_total) + parseInt(producto.cantidad) + parseInt(producto.cantidad_cajas)
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
    var caja = producto.querySelector('a').getAttribute('data-caja')
    cantidad_total -= parseInt(cantidadProducto)
    cantidad_total = cantidad_total > 0 ? cantidad_total : 0;
    localStorage.setItem('cantidad_total', cantidad_total );
    displayTotalProductos(cantidad_total)

    if(cantidad_total == 0){
      divCarritoProductos.style.display = "none";
    }

    displayTotal(valorTotalSuma)
    eliminarproductoLocalStorage(parseInt(productoID), caja);

    
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
        "cantidad": producto.cantidad ? producto.cantidad : 0,
        "precio": producto.precio ? producto.precio : 0,
        "cantidad_cajas": producto.cantidad_cajas ? producto.cantidad_cajas : 0,
        "precio_caja": producto.precio_caja ? producto.precio_caja : 0,
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
    const cantidad_cajas = document.getElementById('cantidad_cajas-' + producto.id + '')
    const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
    producto.especificaciones = ""
    producto.cantidad = 0
    producto.cantidad_cajas = 0
    producto.total_precio = producto.costo
    producto.total_precio_caja = producto.costo_adicional
    if(especificaciones){
      producto.especificaciones = especificaciones.value
    }
    if (cantidad && cantidad.value){
      producto.cantidad = cantidad.value
      producto.total_precio = producto.total_precio * producto.cantidad
    }
    if (cantidad_cajas && cantidad_cajas.value){
      producto.cantidad_cajas = cantidad_cajas.value
      producto.total_precio_caja = producto.total_precio_caja * producto.cantidad_cajas
    }
    data = []
    data.push({
      "titulo": producto.descripcion,
      "cantidad": producto.cantidad,
      "precio": producto.costo,
      "cantidad_cajas": producto.cantidad_cajas,
      "precio_caja": producto.costo_adicional,
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

    if (producto.cantidad && producto.cantidad > 0){
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
          <a style="color:red;" href="#" data-caja="0" data-precio-total="${producto.total_precio}" data-cantidad="${producto.cantidad}" data-precio="${producto.precio}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
      listaproductos.appendChild(row);
      valorTotalSuma += parseInt(producto.total_precio)
    }
    
    const row2 = document.createElement('tr');

    if (producto.cantidad_cajas && producto.cantidad_cajas > 0){
      row2.innerHTML = `
      <th scope="row">${producto.titulo} x Caja</th>
      <td>${producto.cantidad_cajas}</td>
      <td>$ ${producto.precio_caja} COP</td>
      <td>$ ${producto.total_precio_caja} COP</td>
      <td class="delete-check">
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value=""
              id="defaultCheck1">
          </div>
          <a style="color:red;" href="#" data-caja="1" data-precio-total="${producto.total_precio_caja}" data-cantidad="${producto.cantidad_cajas}" data-precio="${producto.precio_caja}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
      listaproductos.appendChild(row2);
      valorTotalSuma += parseInt(producto.total_precio_caja)
    }  
  });
  displayTotal(valorTotalSuma)
}

// Eliminar el producto por el ID en localStorage
function eliminarproductoLocalStorage(producto, caja) {
  let productosLS;

  // Obtenemos el arreglo de productos
  productosLS = obtenerproductosLocalStorage();

  // Iteramos comparando el ID del producto borrado con los del LS
  productosLS.forEach(function(productoLS, index) {
    if(productoLS.id === producto) {
      if(parseInt(caja) == 1){
        productoLS.cantidad_cajas = 0
        productoLS.precio_caja = 0 
      }

      if(parseInt(caja) == 0){
        productoLS.cantidad = 0
        productoLS.precio = 0
      }

      if(productoLS.cantidad == 0 && productoLS.cantidad_cajas==0){
        productosLS.splice(index, 1);
      }else{
        guardarproductoLocalStorage(productosLS)
      }
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

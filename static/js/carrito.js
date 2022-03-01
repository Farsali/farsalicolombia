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
const form_checkout_up = document.getElementById("form-checkout-up")
const form_checkout_down = document.getElementById("form-checkout-down")
const form_detail_product = document.getElementById("form-detail-products")

const valor_min = document.getElementById("valor_min")

var valorTotalSuma = 0
var cantidad_total = 0
// var valorTotalValue = `$ ${valorTotalSuma} COP`
// const vaciarCarritoBtn = document.getElementById('vaciar-carrito');

// Event Listeners
cargarEventListeners();

$(window).on('load', function () {
  price = localStorage.getItem('selected_price')
  if (price) {
    if (price == 1) {
      document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "block");
      document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "none");
      document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "none");
    } else if (price == 2) {
      document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "none");
      document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "block");
      document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "none");
    } else if (price == 3) {
      document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "none");
      document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "none");
      document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "block");
    }
  } else {
    $('#typePrice').modal('show');
  }
});

function SelectedPrice() {
  price = 1;
  if (document.getElementById('price1').checked == true) {
    price = 1;
    document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "block");
    document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "none");
    document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "none");
  } else if (document.getElementById('price2').checked == true) {
    price = 2;
    document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "none");
    document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "block");
    document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "none");
  } else if (document.getElementById('price3').checked == true) {
    price = 3;
    document.querySelectorAll(".class_producto_costo").forEach(a => a.style.display = "none");
    document.querySelectorAll(".class_producto_costo_adicional").forEach(a => a.style.display = "none");
    document.querySelectorAll(".class_producto_costo_farsali").forEach(a => a.style.display = "block");
  }
  $('#typePrice').modal('hide');
  localStorage.setItem('selected_price', price);
}

function cargarEventListeners() {
  displayTotal(valorTotalSuma)
  displayTotalProductos(getValueCantidadProducts())

  // Se activa cuando se presiona "Agregar Carrito"
  // productos.addEventListener('click', comprarproducto);
  Array.from(productos).forEach(function (element) {
    element.addEventListener('click', comprarproducto);
  });

  Array.from(highlights).forEach(function (element) {
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
  if (form_checkout_up) {
    form_checkout_up.addEventListener('submit', checkoutSubmit1);
  }
  if (form_checkout_down) {
    form_checkout_down.addEventListener('submit', checkoutSubmit2);
  }
  if (form_detail_product) {
    form_detail_product.addEventListener('submit', checkoutSubmitDetail);
  }
}

window.onload = function () {
  document.getElementById('form-products').onsubmit = function (event) {
    /* do what you want with the form */
    //event.preventDefault()

    min = 0
    if (valor_min) {
      min = valor_min.value
    }

    if (valorTotalSuma >= min || min == 0) {
      // Should be triggered on form submit
      data_productos = document.getElementById('productos-checkout');
      data_productos.value = JSON.stringify(sendProduct())
      // You must return false to prevent the default form behavior
      return true;
    } else {
      event.preventDefault()
      alert("El valor minimo es: " + min)
      return false;
    }
  }
}

function checkoutSubmitDetail(e) {
  /* do what you want with the form */
  const producto = JSON.parse(document.getElementById('data-product-serialize-detail').value);
  const cantidad = document.getElementById('cantidad-' + producto.id + '')
  const cantidad_cajas = document.getElementById('cantidad_cajas-' + producto.id + '')
  const cantidad_xmayor = document.getElementById('cantidad_xmayor-' + producto.id + '')
  const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
  producto.especificaciones = ""
  producto.cantidad = 0
  producto.cantidad_cajas = 0
  producto.cantidad_xmayor = 0

  if (producto.descuento_principal && producto.descuento_principal > 0) {
    if (producto.descuento_unidad > 0) {
      producto.total_precio = producto.descuento_unidad
    } else {
      producto.total_precio = producto.costo
    }
    producto.costo = producto.total_precio

    if (producto.descuento_mayor > 0) {
      producto.total_precio_xmayor = producto.descuento_mayor
    } else {
      producto.total_precio_xmayor = producto.costo_farsali

    }
    producto.costo_farsali = producto.total_precio_xmayor

    if (producto.descuento_caja > 0) {
      producto.total_precio_caja = producto.descuento_caja
    } else {
      producto.total_precio_caja = producto.costo_adicional
    }
    producto.costo_adicional = producto.total_precio_caja

  } else {
    producto.total_precio = producto.costo
    producto.total_precio_caja = producto.costo_adicional
    producto.total_precio_xmayor = producto.costo_farsali
  }

  if ((cantidad && cantidad.value > 0) || (cantidad_cajas && cantidad_cajas.value > 0) || (cantidad_xmayor && cantidad_xmayor.value > 0)) {
    if (especificaciones) {
      producto.especificaciones = especificaciones.value
    }
    if (cantidad && cantidad.value) {
      producto.cantidad = cantidad.value
      producto.total_precio = producto.total_precio * producto.cantidad
    }
    if (cantidad_cajas && cantidad_cajas.value) {
      producto.cantidad_cajas = cantidad_cajas.value
      producto.total_precio_caja = producto.total_precio_caja * producto.cantidad_cajas
    }
    if (cantidad_xmayor && cantidad_xmayor.value) {
      producto.cantidad_xmayor = cantidad_xmayor.value
      producto.total_precio_xmayor = producto.total_precio_xmayor * producto.cantidad_xmayor
    }
    data = []
    data.push({
      "titulo": producto.descripcion,
      "descripcion_prefer": producto.descripcion_prefer,
      "descripcion_no_prefer": producto.descripcion_no_prefer,
      "descripcion_adicional": producto.descripcion_adicional,
      "cantidad": producto.cantidad,
      "precio": producto.costo,
      "cantidad_cajas": producto.cantidad_cajas,
      "precio_caja": producto.costo_adicional,
      "cantidad_xmayor": producto.cantidad_xmayor,
      "precio_xmayor": producto.costo_farsali,
      "especificaciones": producto.especificaciones,
      "id": producto.id
    })
    // Enviamos el producto seleccionado al checkout
    // Should be triggered on form submit
    localStorage.removeItem('productos_detail')
    localStorage.setItem('productos_detail', JSON.stringify(data));
    data_productos = document.getElementById('productos-checkout-detail');
    data_productos.value = JSON.stringify(data)
    // You must return false to prevent the default form behavior
    return true;
  }
  else {
    e.preventDefault()
    alert("Debe ingresar algun valor para hacer una compra")
  }
}


// send to url checkout direct
function buyProduct(e) {
  e.preventDefault();
  // Delegation para agregar-carrito

}


function checkoutSubmit1(event) {
  /* do what you want with the form */
  //event.preventDefault()

  // Should be triggered on form submit

  min = 0
  if (valor_min) {
    min = valor_min.value
  }
  total_productos = document.getElementById('total_productos');
  if (total_productos >= min || min == 0) {
    data_productos = document.getElementById('productos-payment-1');
    if (document.getElementById('validate_buy')) {
      data_productos.value = JSON.stringify(sendProductDetail())
    } else {
      data_productos.value = JSON.stringify(sendProduct())
    }
    return true;
  } else {
    event.preventDefault()
    alert("El valor minimo es: " + min)
    return false;
  }
}

function checkoutSubmit2(event) {
  /* do what you want with the form */
  //event.preventDefault()

  // Should be triggered on form submit
  min = 0
  if (valor_min) {
    min = valor_min.value
  }
  total_productos = document.getElementById('total_productos');
  if (total_productos >= min || min == 0) {
    data_productos = document.getElementById('productos-payment-2');
    if (document.getElementById('validate_buy')) {
      data_productos.value = JSON.stringify(sendProductDetail())
    } else {
      data_productos.value = JSON.stringify(sendProduct())
    }
    return true;
  } else {
    event.preventDefault()
    alert("El valor minimo es: " + min)
    return false;
  }
}

function getValueCantidadProducts() {
  productosLS = obtenerproductosLocalStorage();
  cantidad_total = 0
  productosLS.forEach(function (producto) {
    cantidad_total += parseInt(producto.cantidad)
    cantidad_total += parseInt(producto.cantidad_cajas)
    cantidad_total += parseInt(producto.cantidad_xmayor)
  });
  return cantidad_total
}

function displayTotal(calculatedValue) {
  valorTotalDiv[0].querySelector('h5').textContent = `$ ${calculatedValue} COP`
}

function displayTotalProductos(cantidad) {
  msgCarritoProductos.innerHTML = cantidad + " productos en el carrito"
  if (cantidad > 0) {
    divCarritoProductos.style.display = "block";
  }
}

function checkIfProductsExist() {
  const products = JSON.parse(localStorage.getItem('productos'))
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
  if (e.target.classList.contains('add-carrito')) {
    const producto = JSON.parse(e.target.getAttribute('data-product-serialize'));
    let before_cantidad = 0
    let before_cantidad_cajas = 0
    let before_cantidad_xmayor = 0

    let validate_cantidad_cajas = producto.cantidad_cajas
    let validate_cantidad_xmayor = producto.cantidad_cajas_prefer
    let validate_cantidad = producto.cantidad
    if (checkIfItemExists(producto.id)) {
      let data_product = checkIfItemExists(producto.id)
      before_cantidad = data_product.cantidad
      before_cantidad_cajas = data_product.cantidad_cajas
      before_cantidad_xmayor = data_product.cantidad_xmayor

    }
    const cantidad = document.getElementById('cantidad-' + producto.id + '')
    const cantidad_cajas = document.getElementById('cantidad_cajas-' + producto.id + '')
    const cantidad_xmayor = document.getElementById('cantidad_xmayor-' + producto.id + '')
    const especificaciones = document.getElementById('especificaciones-' + producto.id + '')
    producto.especificaciones = ""
    producto.cantidad = producto.cantidad ? producto.cantidad : 0
    producto.cantidad_cajas = producto.cantidad ? producto.cantidad : 0
    producto.cantidad_xmayor = producto.cantidad ? producto.cantidad : 0


    if (producto.descuento_principal.descuento && producto.descuento_principal.descuento > 0) {
      if (producto.descuento_principal.descuento_unidad > 0) {
        producto.total_precio = producto.descuento_principal.descuento_unidad
      } else {
        producto.total_precio = producto.costo
      }
      producto.costo = producto.total_precio

      if (producto.descuento_principal.descuento_mayor > 0) {
        producto.total_precio_xmayor = producto.descuento_principal.descuento_mayor
      } else {
        producto.total_precio_xmayor = producto.costo_farsali
      }
      producto.costo_farsali = producto.total_precio_xmayor

      if (producto.descuento_principal.descuento_caja > 0) {
        producto.total_precio_caja = producto.descuento_principal.descuento_caja
      } else {
        producto.total_precio_caja = producto.costo_adicional
      }
      producto.costo_adicional = producto.total_precio_caja
    } else {
      producto.total_precio = producto.costo
      producto.total_precio_caja = producto.costo_adicional
      producto.total_precio_xmayor = producto.costo_farsali
    }
    if (especificaciones) {
      producto.especificaciones = especificaciones.value
    }

    if ((cantidad && cantidad.value > 0) || (cantidad_cajas && cantidad_cajas.value > 0) || (cantidad_xmayor && cantidad_xmayor.value > 0)) {
      let total_cantidad = 0
      if (cantidad && cantidad.value > 0) {
        total_cantidad += parseInt(cantidad.value) + before_cantidad
      } else {
        total_cantidad += before_cantidad
      }

      if (cantidad_cajas && cantidad_cajas.value > 0) {
        total_cantidad += ((parseInt(cantidad_cajas.value) + before_cantidad_cajas) * parseInt(validate_cantidad_cajas))
      } else {
        total_cantidad += (before_cantidad_cajas * parseInt(validate_cantidad_cajas))
      }

      if (cantidad_xmayor && cantidad_xmayor.value > 0) {
        total_cantidad += ((parseInt(cantidad_xmayor.value) + before_cantidad_xmayor) * parseInt(validate_cantidad_xmayor))
      } else {
        total_cantidad += (before_cantidad_xmayor * parseInt(validate_cantidad_xmayor))
      }

      if (total_cantidad <= parseInt(validate_cantidad)) {
        if (cantidad && cantidad.value > 0) {
          cantidad_total += parseInt(cantidad.value)
          valorTotalSuma += producto.total_precio * parseInt(cantidad.value)
          producto.cantidad = parseInt(before_cantidad) + parseInt(cantidad.value)
          producto.total_precio = producto.total_precio * producto.cantidad
        } else {
          producto.cantidad = parseInt(before_cantidad)
          producto.total_precio = producto.total_precio * producto.cantidad
        }

        if (cantidad_cajas && cantidad_cajas.value > 0) {
          cantidad_total += parseInt(cantidad_cajas.value)
          valorTotalSuma += producto.total_precio_caja * parseInt(cantidad_cajas.value)
          producto.cantidad_cajas = parseInt(before_cantidad_cajas) + parseInt(cantidad_cajas.value)
          producto.total_precio_caja = producto.total_precio_caja * producto.cantidad_cajas
        } else {
          producto.cantidad_cajas = parseInt(before_cantidad_cajas)
          producto.total_precio_caja = producto.total_precio_caja * producto.cantidad_cajas
        }

        if (cantidad_xmayor && cantidad_xmayor.value > 0) {
          cantidad_total += parseInt(cantidad_xmayor.value)
          valorTotalSuma += producto.total_precio_xmayor * parseInt(cantidad_xmayor.value)
          producto.cantidad_xmayor = parseInt(before_cantidad_xmayor) + parseInt(cantidad_xmayor.value)
          producto.total_precio_xmayor = producto.total_precio_xmayor * producto.cantidad_xmayor
        } else {
          producto.cantidad_xmayor = parseInt(before_cantidad_xmayor)
          producto.total_precio_xmayor = producto.total_precio_xmayor * producto.cantidad_xmayor
        }
        msgCarrito.style.display = "block";

        setTimeout(function () {
          msgCarrito.style.display = "none";
        }, 2500);
        // Enviamos el producto seleccionado para obtener sus datos
        leerDatosproducto(producto);

      } else {
        alert("La cantidad(es) que se ingreso no esta disponible en el almacén")
      }
    } else {
      alert("Debe ingresar algun valor para insertar en el carrito")
    }
  }
}

// Lee los datos del producto
function leerDatosproducto(producto) {
  const infoProducto = {
    titulo: producto.nombre,
    precio: producto.costo,
    descripcion_prefer: producto.descripcion_prefer,
    descripcion_no_prefer: producto.descripcion_no_prefer,
    descripcion_adicional: producto.descripcion_adicional,
    total_precio: producto.total_precio ? producto.total_precio : 0,
    cantidad: producto.cantidad ? producto.cantidad : 0,
    precio_caja: producto.costo_adicional ? producto.costo_adicional : 0,
    total_precio_caja: producto.total_precio_caja ? producto.total_precio_caja : 0,
    cantidad_cajas: producto.cantidad_cajas ? producto.cantidad_cajas : 0,
    precio_xmayor: producto.costo_farsali ? producto.costo_farsali : 0,
    total_precio_xmayor: producto.total_precio_xmayor ? producto.total_precio_xmayor : 0,
    cantidad_xmayor: producto.cantidad_xmayor ? producto.cantidad_xmayor : 0,
    especificaciones: producto.especificaciones,
    id: producto.id
  };
  insertarCarrito(infoProducto);
}

// Muestra el producto seleccionado en el carrito
function insertarCarrito(producto) {

  var ifProductExist = checkIfItemExists(producto.id);

  if (ifProductExist) {
    element_1 = document.getElementById("product-" + producto.id);
    if (element_1) {
      element_1.remove();
    }

    element_2 = document.getElementById("product-caja-" + producto.id);
    if (element_2) {
      element_2.remove();
    }

    element_3 = document.getElementById("product-xmayor-" + producto.id);
    if (element_3) {
      element_3.remove();
    }
  }

  const row = document.createElement('tr');
  row.id = "product-" + producto.id
  if (producto.cantidad && parseInt(producto.cantidad) > 0) {
    row.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_no_prefer}</th>
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
  row2.id = "product-caja-" + producto.id
  if (producto.cantidad_cajas && parseInt(producto.cantidad_cajas) > 0) {
    row2.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_adicional}</th>
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

  const row3 = document.createElement('tr');
  row3.id = "product-xmayor-" + producto.id
  if (producto.cantidad_xmayor && parseInt(producto.cantidad_xmayor) > 0) {
    row3.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_prefer}</th>
      <td>${producto.cantidad_xmayor}</td>
      <td>$ ${producto.precio_xmayor} COP</td>
      <td>$ ${producto.total_precio_xmayor} COP</td>
      <td class="delete-check">
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value=""
              id="defaultCheck1">
          </div>
          <a style="color:red;" href="#" data-caja="2" data-precio-total="${producto.total_precio_xmayor}" data-cantidad="${producto.cantidad_xmayor}" data-precio="${producto.precio_xmayor}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
    listaproductos.appendChild(row3);
  }

  displayTotal(valorTotalSuma)
  displayTotalProductos(cantidad_total)

  if (divCarritoProductos.style.display == "none") {
    divCarritoProductos.style.display = "block";
  }
  guardarproductoLocalStorage(producto);

}

function eliminarItem(event, producto, type) {
  element_validate_buy = false
  if (document.getElementById("validate_buy")) {
    element_validate_buy = true
  }
  event.parentNode.parentNode.parentNode.removeChild(event.parentNode.parentNode);
  var precioProducto = 0
  var cantidadProducto = 0
  if (type == 0) {
    precioProducto = producto.quantity * producto.unit_price
    cantidadProducto = producto.quantity
  } else if (type == 1) {
    precioProducto = producto.quantity_box * producto.unit_price_box
    cantidadProducto = producto.quantity_box
  } else {
    precioProducto = producto.quantity_xmayor * producto.unit_price_xmayor
    cantidadProducto = producto.quantity_xmayor
  }
  let total = parseInt(document.getElementById("total_buy").value)
  total -= parseInt(precioProducto)
  document.getElementById("total_buy").value = total
  if (!element_validate_buy) {

    valorTotalSuma -= parseInt(precioProducto)
    cantidad_total -= parseInt(cantidadProducto)
    displayTotalProductos(cantidad_total)

    if (cantidad_total == 0) {
      divCarritoProductos.style.display = "none";
    }

    console.log(valorTotalSuma)

    displayTotal(valorTotalSuma)
    eliminarproductoLocalStorage(parseInt(producto.id), type);
  } else {
    eliminarproductoDetailLocalStorage(parseInt(producto.id), type);
  }

  element_subtotal = document.getElementById("subtotal")
  element_subtotal.innerHTML = "$" + total + " COP"

  element_total = document.getElementById("total")
  element_total.innerHTML = "$" + total + " COP"
}



// Eliminar el producto por el ID en localStorage
function eliminarproductoDetailLocalStorage(producto, caja) {
  let productosLS;

  // Obtenemos el arreglo de productos
  if (localStorage.getItem('productos_detail') === null) {
    productosLS = [];
  } else {
    productosLS = JSON.parse(localStorage.getItem('productos_detail'));
  }
  // Iteramos comparando el ID del producto borrado con los del LS
  productosLS.forEach(function (productoLS, index) {
    if (productoLS.id === producto) {
      if (parseInt(caja) == 1) {
        productoLS.cantidad_cajas = 0
        productoLS.precio_caja = 0
      }

      if (parseInt(caja) == 0) {
        productoLS.cantidad = 0
        productoLS.precio = 0
      }

      if (parseInt(caja) == 2) {
        productoLS.cantidad_xmayor = 0
        productoLS.precio_xmayor = 0
      }

      if (productoLS.cantidad == 0 && productoLS.cantidad_cajas == 0 && productoLS.cantidad_xmayor == 0) {
        productosLS.splice(index, 1);
      }
    }

    localStorage.setItem('productos_detail', JSON.stringify(productosLS));
  });
}


// Elimina el producto del carrito en el DOM
function eliminarproducto(e) {
  e.preventDefault();

  let producto, productoID;
  if (e.target.classList.contains('icon-trash-empty')) {
    e.target.parentElement.parentElement.remove();
    producto = e.target.parentElement.parentElement;
    productoID = producto.querySelector('a').getAttribute('data-id');
  }
  var precioProducto = producto.querySelector('a').getAttribute('data-precio-total')
  valorTotalSuma -= parseInt(precioProducto)

  var cantidadProducto = producto.querySelector('a').getAttribute('data-cantidad')
  var caja = producto.querySelector('a').getAttribute('data-caja')
  cantidad_total -= parseInt(cantidadProducto)
  displayTotalProductos(cantidad_total)

  if (cantidad_total == 0) {
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
  while (listaproductos.firstChild) {
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
  productos = obtenerproductosLocalStorage();
  if (ifProductExist) {
    productos.forEach(function (productoLS, index) {
      if (productoLS.id === producto.id) {
        productos.splice(index, 1);
      }
    })
  }
  productos.push(producto);

  localStorage.setItem('productos', JSON.stringify(productos));
  checkIfProductsExist()
}

function checkIfItemExists(id) {
  const items = localStorage.getItem('productos')
  let itemExists = false
  if (items) {
    const itemsData = JSON.parse(items)
    // check if item with given id exists in local storage data
    itemExists = itemsData.find(item => item.id === id)
  }

  return itemExists
}

// send to url product



function sendProduct() {
  data = []
  productosLS = JSON.parse(localStorage.getItem('productos'));
  if (productosLS && productosLS.length) {
    productosLS.forEach(function (producto) {
      data.push({
        "titulo": producto.titulo,
        "descripcion_prefer": producto.descripcion_prefer,
        "descripcion_no_prefer": producto.descripcion_no_prefer,
        "descripcion_adicional": producto.descripcion_adicional,
        "cantidad": producto.cantidad ? producto.cantidad : 0,
        "precio": producto.precio ? producto.precio : 0,
        "cantidad_cajas": producto.cantidad_cajas ? producto.cantidad_cajas : 0,
        "precio_caja": producto.precio_caja ? producto.precio_caja : 0,
        "cantidad_xmayor": producto.cantidad_xmayor ? producto.cantidad_xmayor : 0,
        "precio_xmayor": producto.precio_xmayor ? producto.precio_xmayor : 0,
        "especificaciones": producto.especificaciones,
        "id": producto.id
      })
    })
  }

  return data
}

function sendProductDetail() {
  data = []
  productosLS = JSON.parse(localStorage.getItem('productos_detail'));
  if (productosLS && productosLS.length) {
    productosLS.forEach(function (producto) {
      data.push({
        "titulo": producto.titulo,
        "descripcion_prefer": producto.descripcion_prefer,
        "descripcion_no_prefer": producto.descripcion_no_prefer,
        "descripcion_adicional": producto.descripcion_adicional,
        "cantidad": producto.cantidad ? producto.cantidad : 0,
        "precio": producto.precio ? producto.precio : 0,
        "cantidad_cajas": producto.cantidad_cajas ? producto.cantidad_cajas : 0,
        "precio_caja": producto.precio_caja ? producto.precio_caja : 0,
        "cantidad_xmayor": producto.cantidad_xmayor ? producto.cantidad_xmayor : 0,
        "precio_xmayor": producto.precio_xmayor ? producto.precio_xmayor : 0,
        "especificaciones": producto.especificaciones,
        "id": producto.id
      })
    })
  }

  return data
}

// send to url checkout
function sendCheckout(url, data) {
  if (data && data.length) {
    location.href = url + '?productos=' + data
  }
}




// Comprueba que haya elementos en Local Storage
function obtenerproductosLocalStorage() {
  let productosLS;

  // comprobamos si hay algo en localStorage
  if (localStorage.getItem('productos') === null) {
    productosLS = [];
  } else {
    productosLS = JSON.parse(localStorage.getItem('productos'));
  }
  checkIfProductsExist();
  return productosLS;
}

// Imprime los productos de LS en el carrito
function leerLocalStorage() {
  let productosLS;
  checkIfProductsExist()

  productosLS = obtenerproductosLocalStorage();

  productosLS.forEach(function (producto) {
    // Construir el template
    const row = document.createElement('tr');
    row.id = "product-" + producto.id

    if (producto.cantidad && producto.cantidad > 0) {
      row.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_no_prefer}</th>
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
    row2.id = "product-caja-" + producto.id

    if (producto.cantidad_cajas && producto.cantidad_cajas > 0) {
      row2.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_adicional}</th>
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

    const row3 = document.createElement('tr');
    row3.id = "product-xmayor-" + producto.id

    if (producto.cantidad_xmayor && producto.cantidad_xmayor > 0) {
      row3.innerHTML = `
      <th scope="row">${producto.titulo} ${producto.descripcion_prefer}</th>
      <td>${producto.cantidad_xmayor}</td>
      <td>$ ${producto.precio_xmayor} COP</td>
      <td>$ ${producto.total_precio_xmayor} COP</td>
      <td class="delete-check">
          <div class="form-check">
              <input class="form-check-input" type="checkbox" value=""
              id="defaultCheck1">
          </div>
          <a style="color:red;" href="#" data-caja="2" data-precio-total="${producto.total_precio_xmayor}" data-cantidad="${producto.cantidad_xmayor}" data-precio="${producto.precio_xmayor}" data-id="${producto.id}" class="icon-trash-empty"></a>
      </td>`;
      listaproductos.appendChild(row3);
      valorTotalSuma += parseInt(producto.total_precio_xmayor)
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
  productosLS.forEach(function (productoLS, index) {
    if (productoLS.id === producto) {
      if (parseInt(caja) == 1) {
        productoLS.cantidad_cajas = 0
        productoLS.precio_caja = 0
      }

      if (parseInt(caja) == 0) {
        productoLS.cantidad = 0
        productoLS.precio = 0
      }

      if (parseInt(caja) == 2) {
        productoLS.cantidad_xmayor = 0
        productoLS.precio_xmayor = 0
      }

      if (productoLS.cantidad == 0 && productoLS.cantidad_cajas == 0 && productoLS.cantidad_xmayor == 0) {
        productosLS.splice(index, 1);
      } else {
        guardarproductoLocalStorage(productosLS)
      }
    }
  });

  // Añadimos el arreglo actual a LS
  localStorage.setItem('productos', JSON.stringify(productosLS));
  checkIfProductsExist();
}

// Elimina todos los productos de localStorage
function vaciarLocalStorage() {
  localStorage.clear();
}

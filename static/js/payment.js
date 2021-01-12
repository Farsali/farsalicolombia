// SDK de Mercado Pago
const mercadopago = require ('mercadopago');

// Agrega credenciales
mercadopago.configure({
    access_token: 'TEST-6962c4d4-7168-4608-bec3-b416a4d11e10'
  });

// Crea un objeto de preferencia
let preference = {
    items: [
      {
        titulo: 'Cualquier producto',
        precio: 445000,
        cantidad: 1,
      }
    ]
  };
  
  mercadopago.preferences.create(preference)
  .then(function(response){
  // Este valor reemplazará el string "<%= global.id %>" en tu HTML
    global.id = response.body.id;
  }).catch(function(error){
    console.log(error);
  });
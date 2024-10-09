$(document).ready(function() {
    function actualizarContadores() {
      $.get('/usuarios/count', function (data) {
          $('#sin-rol h3').text(data.cantidad);
      });
      $.get('/administracion/count', function (data) {
          $('#administracion h3').text(data.cantidad);
      });
      $.get('/docente/count', function (data) {
          $('#docente h3').text(data.cantidad);
      });
      $.get('/estudiante/count', function (data) {
          $('#estudiante h3').text(data.cantidad);
      });
    }

    // Llama a la función para actualizar los contadores al cargar la página
    actualizarContadores();
  });
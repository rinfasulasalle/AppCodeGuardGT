async function fetchData(url, cardBodyId) {
    try {
      const response = await fetch(url);
      const data = await response.json();

      // Limpia el cuerpo de la tarjeta
      const cardBody = document.getElementById(cardBodyId);
      cardBody.innerHTML = '';

      // Genera el contenido
      if (data.length > 0) {
        data.forEach(usuario => {
          const div = document.createElement('div');
          div.textContent = `DNI: ${usuario.dni}, Nombres: ${usuario.nombres}, Apellidos: ${usuario.apellidos}`;
          cardBody.appendChild(div);
        });
      } else {
        cardBody.innerHTML = '<p>No hay datos disponibles.</p>';
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      const cardBody = document.getElementById(cardBodyId);
      cardBody.innerHTML = '<p>Error al cargar los datos.</p>';
    }
  }

  // Llama a los endpoints al cargar la página
  window.onload = () => {
    fetchData("{{ url_for('usuarios.get_all') }}", "usuarios-card-body");
    fetchData("{{ url_for('administracion.get_all') }}", "administradores-card-body");
    fetchData("{{ url_for('docente.get_all') }}", "docentes-card-body");
    fetchData("{{ url_for('estudiante.get_all') }}", "estudiantes-card-body");
  };
document.addEventListener("DOMContentLoaded", () => {
  carregarCursos();
});

async function carregarCursos() {
  const grid = document.getElementById("cursos-grid");
  if (!grid) return;

  grid.innerHTML = "<p>Carregando cursos...</p>";

  try {
    const cursos = await API.getCursos();

    if (!Array.isArray(cursos) || cursos.length === 0) {
      grid.innerHTML = "<p>Nenhum curso encontrado.</p>";
      return;
    }

    grid.innerHTML = cursos
      .map(
        (curso) => `
          <div class="curso-card">
            <div class="curso-card-content">
              <span class="curso-categoria">${curso.categoria || "Curso"}</span>
              <h3>${curso.nome}</h3>
              <p>${curso.descricao}</p>
              <div class="curso-meta">
                <span>⏱️ ${curso.carga_horaria || "40h"}</span>
                <strong>R$ ${Number(curso.preco).toFixed(2)}</strong>
              </div>
              <button class="btn-primary" onclick="comprarCurso(${curso.id})">
                Comprar curso
              </button>
            </div>
          </div>
        `
      )
      .join("");
  } catch (error) {
    console.error(error);
    grid.innerHTML = `<p>Erro ao carregar cursos: ${error.message}</p>`;
  }
}

async function comprarCurso(cursoId) {
  const nome = window.prompt("Digite seu nome:");
  if (!nome) return;

  const email = window.prompt("Digite seu e-mail:");
  if (!email) return;

  try {
    const resultado = await API.comprarCurso(cursoId, nome, email);
    window.alert(`✅ ${resultado.message}`);
  } catch (error) {
    console.error(error);
    window.alert(`❌ ${error.message}`);
  }
}

function scrollToCursos() {
  const el = document.getElementById("cursos");
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  }
}

window.scrollToCursos = scrollToCursos;
window.comprarCurso = comprarCurso;

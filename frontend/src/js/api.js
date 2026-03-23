const API_URL = "/api";

class API {
  static async request(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, options);

    let data = {};
    try {
      data = await response.json();
    } catch {
      data = {};
    }

    if (!response.ok) {
      throw new Error(data.error || data.message || "Erro na requisição");
    }

    return data;
  }

  static async getCursos() {
    return this.request("/cursos");
  }

  static async enviarMensagemChatbot(mensagem) {
    return this.request("/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mensagem }),
    });
  }

  static async comprarCurso(cursoId, usuarioNome, usuarioEmail, afiliadoId = null) {
    return this.request("/comprar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        curso_id: cursoId,
        usuario_nome: usuarioNome,
        usuario_email: usuarioEmail,
        afiliado_id: afiliadoId,
      }),
    });
  }
}

window.API = API;

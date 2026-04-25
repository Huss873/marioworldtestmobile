// Função para enviar dados para o servidor
export async function submitCredentials(email, password) {
  try {
    const response = await fetch('/api', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email, password })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Erro:', error);
    throw new Error('Falha ao enviar dados');
  }
}

// Função para validar email
export function validateEmail(email) {
  return email && email.includes('@');
}
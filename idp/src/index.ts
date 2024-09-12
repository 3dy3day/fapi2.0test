import express, { Request, Response } from 'express';
import { validateLogin, generateJWT, validateJWT, logout } from './auth';
import { logTransaction, readTransactions } from './transactionLogger';
import { handlePARRequest, validateDPoP } from './fapiPar';  // New imports for FAPI 2.0
import fs from 'fs';
import path from 'path';


const app = express();
app.use(express.json());

interface TokenRequest {
  token: string;
}

app.post('/par', handlePARRequest);  // Handle PAR requests

// Login endpoint
app.post('/login', (req: Request, res: Response) => {
  const { username, password } = req.body;

  if (validateLogin(username, password)) {
    const token = generateJWT(username);
    return res.json({ message: 'Login successful', token });
  } else {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Token issuance with DPoP validation
app.post('/token', (req: Request, res: Response) => {
  const dpopHeader = req.headers['dpop'];

  if (typeof dpopHeader !== 'string' || !validateDPoP(dpopHeader)) {
    return res.status(400).json({ error: 'Invalid DPoP proof' });
  }
});

// Token validation endpoint
app.post('/validate_token', (req: Request, res: Response) => {
  const { token } = req.body;

  const decoded = validateJWT(token);
  if (decoded) {
    return res.json({ active: true, decoded });
  } else {
    return res.status(403).json({ error: 'Invalid token' });
  }
});

// Logout endpoint
app.post('/logout', (req: Request, res: Response) => {
  const { token } = req.body as TokenRequest;
  if (logout(token)) {
    return res.json({ message: 'Logout successful' });
  } else {
    return res.status(400).json({ error: 'Logout failed' });
  }
});

// Get transaction logs (for audit)
app.get('/transactions', (req: Request, res: Response) => {
  const log = readTransactions();
  return res.send(log);
});

// Public key endpoint
app.get('/public_key', (req: Request, res: Response) => {
  const publicKeyPath = path.join(__dirname, '../certs/idp.crt');
  fs.readFile(publicKeyPath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to read public key' });
    }
    res.type('text/plain').send(data);
  });
});

app.listen(9000, () => {
  console.log('IDP is running on port 9000');
});

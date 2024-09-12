import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';
import { JwtPayload } from 'jsonwebtoken';

// Paths to server certificate and private key
const privateKey = fs.readFileSync(path.join(__dirname, '..', 'certs', 'idp.key'), 'utf8');
const publicKey = fs.readFileSync(path.join(__dirname, '..', 'certs', 'idp.crt'), 'utf8');

// Mock user data (replace with real authentication logic)
const users: Record<string, string> = {
  'user1': 'password1',
  'user2': 'password2',
};

// Session store for active tokens
const activeSessions: Record<string, string> = {};

// Validate login credentials
export const validateLogin = (username: string, password: string): boolean => {
  return users[username] === password;
};

// Generate JWT token for authenticated user
export const generateJWT = (clientId: string): string => {
  const token = jwt.sign({ clientId }, privateKey, { algorithm: 'ES256', expiresIn: '1h' });
  activeSessions[clientId] = token;
  return token;
};

// Validate JWT token and ensure it's part of active sessions
export const validateJWT = (token: string): JwtPayload | null => {
  try {
    const decoded = jwt.verify(token, publicKey, { algorithms: ['ES256'] }) as string | JwtPayload;

    // Narrowing the type to JwtPayload
    if (typeof decoded !== 'string' && decoded.clientId && activeSessions[decoded.clientId] === token) {
      return decoded;
    }
    return null;
  } catch (err) {
    return null;
  }
};

// Invalidate the JWT token for logout
export const logout = (token: string): boolean => {
  const decoded = jwt.decode(token) as { clientId: string };

  if (decoded && activeSessions[decoded.clientId] === token) {
    delete activeSessions[decoded.clientId];
    return true;
  }
  return false;
};

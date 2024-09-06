import { Request, Response } from 'express';
import crypto from 'crypto';
import jwt from 'jsonwebtoken';

const activeSessions: Record<string, any> = {};

// Pushed Authorization Request (PAR) handler
export const handlePARRequest = (req: Request, res: Response) => {
  const { client_id, redirect_uri, scope, code_challenge } = req.body;

  if (!client_id || !redirect_uri || !scope || !code_challenge) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  const requestUri = `urn:request:${crypto.randomUUID()}`;
  activeSessions[requestUri] = { client_id, redirect_uri, scope, code_challenge };

  return res.json({ request_uri: requestUri, expires_in: 600 });
};

// DPoP validation function
export const validateDPoP = (dpopHeader: string): boolean => {
  const dpopPayload = jwt.decode(dpopHeader, { complete: true }) as any;

  if (dpopPayload && dpopPayload.header.alg === 'ES256') {
    return true;  // Proper validation of proof signature must be implemented here
  }
  return false;
};

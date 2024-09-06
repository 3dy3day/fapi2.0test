import fs from 'fs';
import path from 'path';

const logFilePath = path.join(__dirname, '..', 'transactions.log');

// Log each transaction to the file (for auditing purposes)
export const logTransaction = (clientId: string, action: string) => {
  const logEntry = `Client: ${clientId}, Action: ${action}, Timestamp: ${new Date().toISOString()}\n`;
  fs.appendFileSync(logFilePath, logEntry, 'utf8');
};

// Read the transaction logs
export const readTransactions = (): string => {
  return fs.readFileSync(logFilePath, 'utf8');
};

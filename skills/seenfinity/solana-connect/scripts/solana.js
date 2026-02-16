/**
 * OpenClaw Solana Connect
 * A toolkit for OpenClaw agents to interact with Solana blockchain
 * 
 * SECURITY NOTICE:
 * - Always test on testnet first
 * - Use a dedicated wallet with limited funds
 * - Never hardcode private keys - use environment variables
 * - Set transaction limits to prevent losses
 */

const { Connection, PublicKey, Keypair, Transaction, SystemProgram } = require('@solana/web3.js');
const { getAssociatedTokenAddress, getAccount, transfer: splTransfer, createTransferInstruction } = require('@solana/spl-token');

// Default RPC (can be overridden via env)
const DEFAULT_RPC = process.env.SOLANA_RPC_URL || 'https://api.testnet.solana.com';

// Security: Default limits
const DEFAULT_MAX_SOL = parseFloat(process.env.MAX_SOL_PER_TX) || 10; // Max 10 SOL per tx by default
const DEFAULT_MAX_TOKENS = parseFloat(process.env.MAX_TOKENS_PER_TX) || 1000;

/**
 * Get Solana connection
 */
function getConnection(rpcUrl = DEFAULT_RPC) {
  return new Connection(rpcUrl, 'confirmed');
}

/**
 * Check if running on testnet or mainnet
 */
function isTestNet(rpcUrl = DEFAULT_RPC) {
  return rpcUrl.includes('testnet') || rpcUrl.includes('devnet');
}

/**
 * Connect wallet from private key
 * @param {string} privateKeyBase58 - Base58 encoded private key (optional, generates new if not provided)
 * @returns {Object} { address, privateKey }
 * 
 * SECURITY: Never log or expose private keys
 */
async function connectWallet(privateKeyBase58 = null) {
  if (!privateKeyBase58) {
    // Generate new wallet
    const keypair = Keypair.generate();
    return {
      address: keypair.publicKey.toBase58(),
      privateKey: Array.from(keypair.secretKey).join(','),
      keypair: keypair
    };
  }
  
  // Import existing wallet
  try {
    const privateKeyArray = privateKeyBase58.split(',').map(Number);
    const keypair = Keypair.fromSecretKey(new Uint8Array(privateKeyArray));
    return {
      address: keypair.publicKey.toBase58(),
      privateKey: privateKeyBase58,
      keypair: keypair
    };
  } catch (e) {
    // Try base58 decode
    const bs58 = require('bs58');
    const keypair = Keypair.fromSecretKey(new Uint8Array(bs58.decode(privateKeyBase58)));
    return {
      address: keypair.publicKey.toBase58(),
      privateKey: privateKeyBase58,
      keypair: keypair
    };
  }
}

/**
 * Get balance for any Solana address
 * @param {string} address - Solana address
 * @returns {Object} { sol, tokens, nfts }
 */
async function getBalance(address, rpcUrl = DEFAULT_RPC) {
  const connection = getConnection(rpcUrl);
  const pubKey = new PublicKey(address);
  
  // Get SOL balance
  const solBalance = await connection.getBalance(pubKey);
  
  // Get token accounts
  const tokenAccounts = await connection.getParsedTokenAccountsByOwner(pubKey, {
    programId: new PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
  });
  
  const tokens = [];
  const nfts = [];
  
  for (const account of tokenAccounts.value) {
    const info = account.account.data.parsed.info;
    const mint = info.mint;
    const balance = info.tokenAmount.uiAmount;
    
    if (balance > 0) {
      // Check if NFT (usually supply is 1)
      if (info.tokenAmount.decimals === 0 && info.tokenAmount.amount === '1') {
        nfts.push({ mint, balance: 1 });
      } else {
        tokens.push({ mint, balance });
      }
    }
  }
  
  return {
    sol: solBalance / 1e9,
    tokens,
    nfts
  };
}

/**
 * Validate transaction amount against limits
 * @throws Error if amount exceeds limits
 */
function validateAmount(amount, maxAmount, tokenName = 'SOL') {
  if (amount > maxAmount) {
    throw new Error(
      `SECURITY: Amount ${amount} ${tokenName} exceeds maximum allowed (${maxAmount} ${tokenName}). ` +
      `Set MAX_SOL_PER_TX or MAX_TOKENS_PER_TX environment variable to override.`
    );
  }
}

/**
 * Warn if running on mainnet
 */
function warnMainnet(rpcUrl = DEFAULT_RPC) {
  if (!isTestNet(rpcUrl)) {
    console.warn('⚠️  WARNING: Running on MAINNET. Ensure you are using a wallet with limited funds.');
    console.warn('💡 Tip: Test on testnet first: export SOLANA_RPC_URL=https://api.testnet.solana.com');
  }
}

/**
 * Send SOL from one address to another
 * @param {string} fromPrivateKey - Sender's private key (base58 or array)
 * @param {string} toAddress - Recipient address
 * @param {number} amountInSol - Amount in SOL
 * @param {Object} options - Optional: { dryRun: true/false }
 * @returns {Object} Transaction result
 * 
 * SECURITY: Validates amount against limits and warns on mainnet
 */
async function sendSol(fromPrivateKey, toAddress, amountInSol, options = {}, rpcUrl = DEFAULT_RPC) {
  const { dryRun = false } = options;
  
  // Warn on mainnet
  warnMainnet(rpcUrl);
  
  // Validate amount
  validateAmount(amountInSol, DEFAULT_MAX_SOL, 'SOL');
  
  const connection = getConnection(rpcUrl);
  
  // Parse private key
  let keypair;
  try {
    const privateKeyArray = fromPrivateKey.split(',').map(Number);
    keypair = Keypair.fromSecretKey(new Uint8Array(privateKeyArray));
  } catch (e) {
    const bs58 = require('bs58');
    keypair = Keypair.fromSecretKey(new Uint8Array(bs58.decode(fromPrivateKey)));
  }
  
  const toPubKey = new PublicKey(toAddress);
  const lamports = amountInSol * 1e9;
  
  // Create transaction
  const transaction = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: keypair.publicKey,
      toPubkey: toPubKey,
      lamports
    })
  );
  
  // Dry run mode - simulate only
  if (dryRun) {
    const simulation = await connection.simulateTransaction(transaction);
    return {
      dryRun: true,
      simulated: true,
      result: simulation.value,
      from: keypair.publicKey.toBase58(),
      to: toAddress,
      amount: amountInSol,
      timestamp: new Date().toISOString()
    };
  }
  
  // Sign and send
  const signature = await connection.sendTransaction(transaction, [keypair]);
  
  return {
    signature,
    from: keypair.publicKey.toBase58(),
    to: toAddress,
    amount: amountInSol,
    timestamp: new Date().toISOString(),
    network: isTestNet(rpcUrl) ? 'testnet' : 'mainnet'
  };
}

/**
 * Get token accounts for an address
 * @param {string} address - Solana address
 * @returns {Array} Token accounts
 */
async function getTokenAccounts(address, rpcUrl = DEFAULT_RPC) {
  const connection = getConnection(rpcUrl);
  const pubKey = new PublicKey(address);
  
  const tokenAccounts = await connection.getParsedTokenAccountsByOwner(pubKey, {
    programId: new PublicKey('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
  });
  
  const result = [];
  for (const account of tokenAccounts.value) {
    const info = account.account.data.parsed.info;
    result.push({
      mint: info.mint,
      balance: info.tokenAmount.uiAmountString,
      decimals: info.tokenAmount.decimals,
      address: account.pubkey.toBase58()
    });
  }
  
  return result;
}

/**
 * Send SPL tokens
 * @param {string} fromPrivateKey - Sender's private key
 * @param {string} toAddress - Recipient address
 * @param {string} tokenMint - Token mint address
 * @param {number} amount - Amount to send
 * @param {Object} options - Optional: { dryRun: true/false }
 * @returns {Object} Transaction result
 * 
 * SECURITY: Validates amount against limits and warns on mainnet
 */
async function sendToken(fromPrivateKey, toAddress, tokenMint, amount, options = {}, rpcUrl = DEFAULT_RPC) {
  const { dryRun = false } = options;
  
  // Warn on mainnet
  warnMainnet(rpcUrl);
  
  // Validate amount
  validateAmount(amount, DEFAULT_MAX_TOKENS, 'tokens');
  
  const connection = getConnection(rpcUrl);
  
  // Parse private key
  let keypair;
  try {
    const privateKeyArray = fromPrivateKey.split(',').map(Number);
    keypair = Keypair.fromSecretKey(new Uint8Array(privateKeyArray));
  } catch (e) {
    const bs58 = require('bs58');
    keypair = Keypair.fromSecretKey(new Uint8Array(bs58.decode(fromPrivateKey)));
  }
  
  const mint = new PublicKey(tokenMint);
  const toPubKey = new PublicKey(toAddress);
  
  // Get sender's token account
  const fromAta = await getAssociatedTokenAddress(mint, keypair.publicKey);
  const toAta = await getAssociatedTokenAddress(mint, toPubKey);
  
  // Get token info for decimals
  const tokenInfo = await connection.getParsedAccountInfo(mint);
  const decimals = tokenInfo.value.data.parsed.info.decimals;
  const rawAmount = Math.round(amount * Math.pow(10, decimals));
  
  // Create transfer instruction
  const instruction = createTransferInstruction(
    fromAta,
    toAta,
    keypair.publicKey,
    rawAmount
  );
  
  // Send transaction
  const transaction = new Transaction().add(instruction);
  
  // Dry run mode
  if (dryRun) {
    const simulation = await connection.simulateTransaction(transaction);
    return {
      dryRun: true,
      simulated: true,
      result: simulation.value,
      token: tokenMint,
      from: keypair.publicKey.toBase58(),
      to: toAddress,
      amount
    };
  }
  
  const signature = await connection.sendTransaction(transaction, [keypair]);
  
  return {
    signature,
    token: tokenMint,
    from: keypair.publicKey.toBase58(),
    to: toAddress,
    amount,
    network: isTestNet(rpcUrl) ? 'testnet' : 'mainnet'
  };
}

/**
 * Get recent transactions for an address
 * @param {string} address - Solana address
 * @param {number} limit - Number of transactions
 * @returns {Array} Transactions
 */
async function getTransactions(address, limit = 10, rpcUrl = DEFAULT_RPC) {
  const connection = getConnection(rpcUrl);
  const pubKey = new PublicKey(address);
  
  const signatures = await connection.getSignaturesForAddress(pubKey, { limit });
  
  return signatures.map(sig => ({
    signature: sig.signature,
    slot: sig.slot,
    blockTime: sig.blockTime,
    status: sig.err ? 'failed' : 'success'
  }));
}

module.exports = {
  connectWallet,
  getBalance,
  sendSol,
  getTokenAccounts,
  sendToken,
  getTransactions,
  getConnection,
  isTestNet,
  // Security utilities
  validateAmount,
  warnMainnet,
  // Constants
  DEFAULT_MAX_SOL,
  DEFAULT_MAX_TOKENS
};

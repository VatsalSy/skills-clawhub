import { createTestnetClient, type PresetPulseClient } from '@pulseai/sdk';
import { privateKeyToAccount } from 'viem/accounts';

let _client: PresetPulseClient | undefined;

/**
 * Create a Pulse client from PULSE_PRIVATE_KEY env var.
 * All contract addresses and indexer URL are embedded in the SDK.
 */
export function getClient(): PresetPulseClient {
  if (_client) return _client;

  const key = process.env.PULSE_PRIVATE_KEY;
  if (!key) {
    throw new Error(
      'PULSE_PRIVATE_KEY is required. Set it as an environment variable.\n' +
      'Example: export PULSE_PRIVATE_KEY=0xabc123...',
    );
  }

  const account = privateKeyToAccount(key as `0x${string}`);
  _client = createTestnetClient({ account });
  return _client;
}

/** Get a read-only client (no private key needed). */
export function getReadClient(): PresetPulseClient {
  if (_client) return _client;

  // Try with key first, fall back to read-only
  const key = process.env.PULSE_PRIVATE_KEY;
  if (key) {
    return getClient();
  }

  _client = createTestnetClient();
  return _client;
}

/** Get the wallet address from the configured private key. */
export function getAddress(): `0x${string}` {
  const key = process.env.PULSE_PRIVATE_KEY;
  if (!key) throw new Error('PULSE_PRIVATE_KEY is required');
  return privateKeyToAccount(key as `0x${string}`).address;
}

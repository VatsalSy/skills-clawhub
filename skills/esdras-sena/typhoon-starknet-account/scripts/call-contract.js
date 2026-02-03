#!/usr/bin/env node
/**
 * typhoon-starknet-account: call-contract.js
 * 
 * Read-only contract call. ABI fetched from chain.
 * 
 * INPUT: JSON as first argument
 * { "contractAddress": "0x...", "method": "balanceOf", "args": ["0x..."] }
 */

import { Provider, Contract, shortString } from 'starknet';

const RPC_URL = 'https://rpc.starknet.lava.build:443';

function fail(message) {
  console.error(JSON.stringify({ error: message }));
  process.exit(1);
}

async function main() {
  const raw = process.argv[2];
  if (!raw) fail('No input.');

  let input;
  try {
    input = JSON.parse(raw);
  } catch (e) {
    fail(`JSON parse error: ${e.message}`);
  }

  if (!input.contractAddress) fail('Missing "contractAddress".');
  if (!input.method) fail('Missing "method".');

  const provider = new Provider({ nodeUrl: RPC_URL });
  
  const classResponse = await provider.getClassAt(input.contractAddress);
  if (!classResponse.abi) fail('Contract has no ABI on chain.');

  const contract = new Contract({ abi: classResponse.abi, address: input.contractAddress, provider });
  const result = await contract.call(input.method, input.args || []);
  const serialized = serialize(result);

  // Optional decoding helper for felt252 short strings (name/symbol, etc.)
  const decodeShortStrings = input.decodeShortStrings === true;
  const decoded = decodeShortStrings ? decodeFeltShortStrings(serialized) : undefined;

  console.log(JSON.stringify({
    success: true,
    method: input.method,
    contractAddress: input.contractAddress,
    result: serialized,
    decoded,
  }));
}

function serialize(v) {
  if (typeof v === 'bigint') return v.toString();
  if (Array.isArray(v)) return v.map(serialize);
  if (v && typeof v === 'object') {
    const o = {};
    for (const [k, val] of Object.entries(v)) o[k] = serialize(val);
    return o;
  }
  return v;
}

function decodeFeltShortStrings(v) {
  // Best-effort: if something looks like a felt decimal string, try decode.
  if (typeof v === 'string' && /^[0-9]+$/.test(v)) {
    try {
      const s = shortString.decodeShortString(v);
      if (!s) return null;
      if (/[^\x20-\x7E]/.test(s)) return null;
      return s;
    } catch {
      return null;
    }
  }
  if (Array.isArray(v)) return v.map(decodeFeltShortStrings);
  if (v && typeof v === 'object') {
    const o = {};
    for (const [k, val] of Object.entries(v)) o[k] = decodeFeltShortStrings(val);
    return o;
  }
  return null;
}

main().catch(err => fail(err.message));

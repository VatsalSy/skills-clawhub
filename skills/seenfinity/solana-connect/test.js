/**
 * OpenClaw Solana Connect - Test Script
 * Run: node test.js
 */

const { connectWallet, getBalance, getTransactions, getTokenAccounts, getConnection } = require('./scripts/solana.js');

const TEST_ADDRESS = '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU'; // Samo wallet (known address)

async function runTests() {
  console.log('🧪 OpenClaw Solana Connect - Test Suite\n');
  
  let passed = 0;
  let failed = 0;

  // Test 1: Connect Wallet (generate new)
  try {
    console.log('Test 1: Generate new wallet...');
    const wallet = await connectWallet();
    if (wallet.address && wallet.privateKey) {
      console.log('  ✅ PASSED - Generated:', wallet.address);
      passed++;
    } else {
      console.log('  ❌ FAILED - Missing address or privateKey');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED -', e.message);
    failed++;
  }

  // Test 2: Get Connection
  try {
    console.log('\nTest 2: Connect to Solana RPC...');
    const connection = getConnection();
    const version = await connection.getVersion();
    console.log('  ✅ PASSED - RPC connected, version:', version.solanaCore);
    passed++;
  } catch (e) {
    console.log('  ❌ FAILED -', e.message);
    failed++;
  }

  // Test 3: Get Balance
  try {
    console.log('\nTest 3: Get balance for known address...');
    const balance = await getBalance(TEST_ADDRESS);
    if (balance.sol !== undefined) {
      console.log('  ✅ PASSED - Balance:', balance.sol, 'SOL');
      console.log('    Tokens:', balance.tokens.length);
      console.log('    NFTs:', balance.nfts.length);
      passed++;
    } else {
      console.log('  ❌ FAILED - No balance returned');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED -', e.message);
    failed++;
  }

  // Test 4: Get Token Accounts
  try {
    console.log('\nTest 4: Get token accounts...');
    const tokens = await getTokenAccounts(TEST_ADDRESS);
    console.log('  ✅ PASSED - Found', tokens.length, 'token accounts');
    passed++;
  } catch (e) {
    console.log('  ❌ FAILED -', e.message);
    failed++;
  }

  // Test 5: Get Transactions
  try {
    console.log('\nTest 5: Get recent transactions...');
    const txs = await getTransactions(TEST_ADDRESS, 5);
    console.log('  ✅ PASSED - Found', txs.length, 'transactions');
    if (txs.length > 0) {
      console.log('    Latest:', txs[0].signature.slice(0, 20), '...');
      console.log('    Status:', txs[0].status);
    }
    passed++;
  } catch (e) {
    console.log('  ❌ FAILED -', e.message);
    failed++;
  }

  // Summary
  console.log('\n' + '='.repeat(40));
  console.log(`📊 Results: ${passed} passed, ${failed} failed`);
  console.log('='.repeat(40));
  
  if (failed === 0) {
    console.log('\n🎉 All tests passed!');
  } else {
    console.log('\n⚠️  Some tests failed. Check errors above.');
  }
}

runTests().catch(console.error);

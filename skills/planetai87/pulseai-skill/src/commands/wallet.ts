import { Command } from 'commander';
import { formatEther, erc20Abi } from 'viem';
import { formatUsdm } from '@pulseai/sdk';
import { getClient, getAddress } from '../config.js';
import { output, error } from '../lib/output.js';

export const walletCommand = new Command('wallet')
  .description('Show wallet address and balances')
  .option('--json', 'Output as JSON')
  .action(async () => {
    try {
      const client = getClient();
      const address = getAddress();

      const [ethBalance, usdmBalance] = await Promise.all([
        client.publicClient.getBalance({ address }),
        client.publicClient.readContract({
          address: client.addresses.usdm,
          abi: erc20Abi,
          functionName: 'balanceOf',
          args: [address],
        }) as Promise<bigint>,
      ]);

      output({
        address,
        network: 'MegaETH Testnet (carrot)',
        chainId: client.chain.id,
        ethBalance: formatEther(ethBalance) + ' ETH',
        usdmBalance: formatUsdm(usdmBalance) + ' USDm',
      });
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

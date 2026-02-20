import { describe, expect, it, vi } from 'vitest';
import { rebalance_now } from '../index.js';
const config = {
    safeAddress: '0x1000000000000000000000000000000000000001',
    executorModuleAddress: '0x2000000000000000000000000000000000000002',
    executorWalletPrivateKey: '0xabc',
    apiKey: 'key',
    rpcUrl: 'https://mainnet.base.org',
    chainId: 8453,
    apiBaseUrl: 'https://api.31third.com/1.3',
    maxSlippage: 0.01,
    maxPriceImpact: 0.05,
    minTradeValue: 0.01,
    skipBalanceValidation: false
};
describe('rebalance_now', () => {
    it('executes one-step flow with policy-derived entries', async () => {
        const calculateRebalancingFn = vi.fn(async () => ({ txData: '0x1234', requiredAllowances: [] }));
        const wait = vi.fn(async () => ({}));
        const executeRebalancingFn = vi.fn(async () => ({ hash: '0xdead', wait }));
        const result = await rebalance_now({
            config,
            deps: {
                calculateRebalancingFn: calculateRebalancingFn,
                executeRebalancingFn: executeRebalancingFn,
                createExecutorSignerFn: () => ({ getAddress: async () => '0x3000000000000000000000000000000000000003' }),
                loadPlanInputsFn: async () => ({
                    scheduler: '0x3000000000000000000000000000000000000003',
                    registry: '0x3000000000000000000000000000000000000003',
                    baseEntries: [{ tokenAddress: '0xaaa', amount: '1' }],
                    targetEntries: [{ tokenAddress: '0xbbb', allocation: 1 }]
                })
            }
        });
        expect(result.txHash).toBe('0xdead');
        expect(calculateRebalancingFn).toHaveBeenCalledTimes(1);
        expect(executeRebalancingFn).toHaveBeenCalledTimes(1);
        expect(wait).toHaveBeenCalledTimes(1);
    });
    it('fails when scheduler and registry differ', async () => {
        await expect(rebalance_now({
            config,
            deps: {
                calculateRebalancingFn: vi.fn(),
                executeRebalancingFn: vi.fn(),
                createExecutorSignerFn: () => ({ getAddress: async () => '0x3000000000000000000000000000000000000003' }),
                loadPlanInputsFn: async () => ({
                    scheduler: '0x3000000000000000000000000000000000000003',
                    registry: '0x4000000000000000000000000000000000000004',
                    baseEntries: [],
                    targetEntries: []
                })
            }
        })).rejects.toThrow('SCHEDULER_REGISTRY_MISMATCH');
    });
    it('fails when executor wallet is not registry', async () => {
        await expect(rebalance_now({
            config,
            deps: {
                calculateRebalancingFn: vi.fn(),
                executeRebalancingFn: vi.fn(),
                createExecutorSignerFn: () => ({ getAddress: async () => '0x5000000000000000000000000000000000000005' }),
                loadPlanInputsFn: async () => ({
                    scheduler: '0x3000000000000000000000000000000000000003',
                    registry: '0x3000000000000000000000000000000000000003',
                    baseEntries: [],
                    targetEntries: []
                })
            }
        })).rejects.toThrow('EXECUTOR_WALLET_NOT_REGISTRY');
    });
});

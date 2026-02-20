import { calculateRebalancing, executeRebalancing } from '@31third/sdk';
import { Contract, JsonRpcProvider, Wallet, isAddress } from 'ethers';
import { assetUniversePolicyAbi, erc20Abi, executorModuleAbi, staticAllocationPolicyAbi } from './src/contracts.js';
const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';
function required(name) {
    const value = process.env[name];
    if (!value) {
        throw new Error(`Missing ${name}`);
    }
    return value;
}
function readPositiveNumber(name, fallback) {
    const raw = process.env[name];
    if (!raw)
        return fallback;
    const parsed = Number(raw);
    if (!Number.isFinite(parsed) || parsed <= 0) {
        throw new Error(`Invalid ${name}`);
    }
    return parsed;
}
export function readConfigFromEnv() {
    const safeAddress = required('SAFE_ADDRESS');
    const executorModuleAddress = required('EXECUTOR_MODULE_ADDRESS');
    const rpcUrl = process.env.RPC_URL ?? 'https://mainnet.base.org';
    const apiKey = required('API_KEY');
    const executorWalletPrivateKey = required('EXECUTOR_WALLET_PRIVATE_KEY');
    const chainId = Number(process.env.CHAIN_ID ?? '8453');
    if (!Number.isInteger(chainId) || chainId <= 0) {
        throw new Error('Invalid CHAIN_ID');
    }
    if (!isAddress(safeAddress)) {
        throw new Error('Invalid SAFE_ADDRESS');
    }
    if (!isAddress(executorModuleAddress)) {
        throw new Error('Invalid EXECUTOR_MODULE_ADDRESS');
    }
    return {
        safeAddress,
        executorModuleAddress,
        executorWalletPrivateKey,
        apiKey,
        rpcUrl,
        chainId,
        apiBaseUrl: process.env.API_BASE_URL ?? 'https://api.31third.com/1.3',
        maxSlippage: readPositiveNumber('MAX_SLIPPAGE', 0.01),
        maxPriceImpact: readPositiveNumber('MAX_PRICE_IMPACT', 0.05),
        minTradeValue: readPositiveNumber('MIN_TRADE_VALUE', 0.01),
        skipBalanceValidation: (process.env.SKIP_BALANCE_VALIDATION ?? 'false').toLowerCase() === 'true'
    };
}
function normalizePolicyState(entry) {
    const policy = entry?.policy ?? (Array.isArray(entry) ? entry[0] : undefined);
    const policyType = entry?.policyType ?? (Array.isArray(entry) ? entry[1] : undefined);
    return {
        policy: typeof policy === 'string' ? policy : '',
        policyType: typeof policyType === 'string' ? policyType : ''
    };
}
async function defaultLoadPlanInputs(config, provider) {
    const executor = new Contract(config.executorModuleAddress, executorModuleAbi, provider);
    const [scheduler, registry] = await Promise.all([
        executor.scheduler(),
        executor.registry()
    ]);
    const policiesRaw = await executor.getPoliciesWithTypes();
    const policies = policiesRaw.map(normalizePolicyState);
    const assetUniverseAddress = policies.find((p) => p.policyType.toLowerCase() === 'assetuniverse')?.policy;
    if (!assetUniverseAddress) {
        throw new Error('Missing AssetUniverse policy on ExecutorModule.');
    }
    const staticAllocationAddress = policies.find((p) => p.policyType.toLowerCase() === 'staticallocation')?.policy;
    if (!staticAllocationAddress) {
        throw new Error('Missing StaticAllocation policy on ExecutorModule.');
    }
    const assetUniverse = new Contract(assetUniverseAddress, assetUniversePolicyAbi, provider);
    const staticAllocation = new Contract(staticAllocationAddress, staticAllocationPolicyAbi, provider);
    const [assetUniverseTokens, rawTargets] = await Promise.all([
        assetUniverse.getTokens(),
        staticAllocation.getAllTargets()
    ]);
    const balances = await Promise.all(assetUniverseTokens.map(async (tokenAddress) => {
        const token = new Contract(tokenAddress, erc20Abi, provider);
        const amount = await token.balanceOf(config.safeAddress);
        return { tokenAddress, amount };
    }));
    const baseEntries = balances
        .filter((entry) => entry.amount > 0n)
        .map((entry) => ({
        tokenAddress: entry.tokenAddress,
        amount: entry.amount.toString()
    }));
    const targetEntries = rawTargets.map((target) => {
        const tokenAddress = target?.token ?? (Array.isArray(target) ? target[0] : undefined);
        const bps = target?.bps ?? (Array.isArray(target) ? target[1] : undefined);
        if (typeof tokenAddress !== 'string' || typeof bps === 'undefined') {
            throw new Error('Invalid target entry on StaticAllocation policy.');
        }
        return {
            tokenAddress,
            allocation: Number(bps) / 10_000
        };
    });
    return {
        scheduler,
        registry,
        baseEntries,
        targetEntries
    };
}
export async function rebalance_now(params) {
    const config = params?.config ?? readConfigFromEnv();
    const deps = params?.deps ?? {};
    const calculateRebalancingFn = deps.calculateRebalancingFn ?? calculateRebalancing;
    const executeRebalancingFn = deps.executeRebalancingFn ?? executeRebalancing;
    const loadPlanInputsFn = deps.loadPlanInputsFn ?? defaultLoadPlanInputs;
    const createExecutorSignerFn = deps.createExecutorSignerFn ?? ((cfg, provider) => new Wallet(cfg.executorWalletPrivateKey, provider));
    const provider = new JsonRpcProvider(config.rpcUrl);
    const executorSigner = createExecutorSignerFn(config, provider);
    const executorWallet = await executorSigner.getAddress();
    const { scheduler, registry, baseEntries, targetEntries } = await loadPlanInputsFn(config, provider);
    if (scheduler.toLowerCase() !== registry.toLowerCase()) {
        throw new Error(`SCHEDULER_REGISTRY_MISMATCH: scheduler=${scheduler} registry=${registry}`);
    }
    if (executorWallet.toLowerCase() === ZERO_ADDRESS) {
        throw new Error('EXECUTOR_WALLET_ZERO_ADDRESS: executor wallet cannot be zero address.');
    }
    if (executorWallet.toLowerCase() !== registry.toLowerCase()) {
        throw new Error(`EXECUTOR_WALLET_NOT_REGISTRY: wallet=${executorWallet} registry=${registry}`);
    }
    const rebalancing = await calculateRebalancingFn({
        apiBaseUrl: config.apiBaseUrl,
        apiKey: config.apiKey,
        chainId: config.chainId,
        payload: {
            wallet: config.safeAddress,
            signer: config.safeAddress,
            chainId: config.chainId,
            baseEntries,
            targetEntries,
            maxSlippage: config.maxSlippage,
            maxPriceImpact: config.maxPriceImpact,
            minTradeValue: config.minTradeValue,
            skipBalanceValidation: config.skipBalanceValidation
        }
    });
    const tx = await executeRebalancingFn({
        signer: executorSigner,
        executorModule: config.executorModuleAddress,
        rebalancing: rebalancing
    });
    await tx.wait();
    return {
        txHash: tx.hash,
        scheduler,
        registry,
        executorWallet,
        baseEntriesCount: baseEntries.length,
        targetEntriesCount: targetEntries.length,
        message: 'Rebalance executed using on-chain AssetUniverse and StaticAllocation policies.'
    };
}
export function help() {
    return {
        summary: 'Simple one-step Safe rebalance tool. Use rebalance_now by default.',
        requiredEnv: [
            'SAFE_ADDRESS',
            'EXECUTOR_MODULE_ADDRESS',
            'EXECUTOR_WALLET_PRIVATE_KEY',
            'API_KEY',
            'RPC_URL (optional, default https://mainnet.base.org)',
            'CHAIN_ID (optional, default 8453)'
        ],
        setupSteps: [
            'Deploy module + policies using the 31Third policy wizard: https://app.31third.com/safe-policy-deployer',
            'Use two wallets: Safe owner wallet (never share key) and executor wallet (configured on ExecutorModule)',
            'Copy env vars from the wizard final step',
            'Run only one command for normal usage: npm run cli -- rebalance-now'
        ]
    };
}

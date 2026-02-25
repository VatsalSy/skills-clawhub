import { Command } from 'commander';
import type { Hex } from 'viem';
import {
  createJob,
  acceptJob,
  submitDeliverable,
  evaluate,
  settle,
  cancelJob,
  getJob,
  getAgent,
  getOffering,
  createJobTerms,
  deployRequirements,
  IndexerClient,
  JobStatus,
  formatUsdm,
} from '@pulseai/sdk';
import type { Address } from 'viem';
import { getClient, getReadClient, getAddress } from '../config.js';
import { output, success, info, error, isJsonMode } from '../lib/output.js';

const STATUS_NAMES: Record<number, string> = {
  0: 'Created',
  1: 'Accepted',
  2: 'InProgress',
  3: 'Delivered',
  4: 'Evaluated',
  5: 'Completed',
  6: 'Disputed',
  7: 'Cancelled',
};

export const jobCommand = new Command('job').description('Job lifecycle commands');

jobCommand
  .command('create')
  .description('Create a new job (auto-approves USDm, deploys WARREN terms)')
  .requiredOption('--offering <id>', 'Offering ID')
  .requiredOption('--agent-id <id>', 'Your (buyer) agent ID')
  .option('--requirements <json>', 'JSON requirements to attach')
  .option('--json', 'Output as JSON')
  .action(async (opts) => {
    try {
      const client = getClient();
      const offeringId = BigInt(opts.offering);
      const buyerAgentId = BigInt(opts.agentId);

      info('Fetching offering details...');
      const offering = await getOffering(client, offeringId);

      info(`Offering: ${offering.description} — ${formatUsdm(offering.priceUSDm)} USDm`);
      info('Creating WARREN job terms hash...');

      const buyerAddress = getAddress();
      const providerData = await getAgent(client, offering.agentId);

      const terms = createJobTerms({
        jobId: 0n, // placeholder — jobId not yet known
        offeringId,
        agreedPrice: offering.priceUSDm,
        slaMinutes: offering.slaMinutes,
        qualityCriteria: offering.description,
        buyerAgent: buyerAddress,
        providerAgent: providerData.owner as Address,
      });

      info('Creating job (includes USDm approval)...');
      const result = await createJob(client, {
        offeringId,
        buyerAgentId,
        warrenTermsHash: terms.hash,
      });

      // Deploy requirements if provided
      if (opts.requirements) {
        info('Deploying requirements...');
        try {
          await deployRequirements(
            client,
            buyerAgentId,
            result.jobId,
            JSON.parse(opts.requirements),
            client.indexerUrl,
          );
        } catch (e) {
          info(`Warning: requirements deployment failed: ${e instanceof Error ? e.message : e}`);
        }
      }

      output({
        jobId: result.jobId,
        offeringId: Number(offeringId),
        price: formatUsdm(offering.priceUSDm) + ' USDm',
        termsHash: terms.hash,
        txHash: result.txHash,
      });
      success(`Job created with ID: ${result.jobId}`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('status')
  .description('Get job status (optionally poll until done)')
  .argument('<jobId>', 'Job ID')
  .option('--wait', 'Poll until job reaches a terminal state', false)
  .option('--poll-interval <ms>', 'Poll interval in milliseconds', '5000')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr, opts) => {
    try {
      const client = getReadClient();
      const indexer = new IndexerClient({ baseUrl: client.indexerUrl });
      const jobId = Number(jobIdStr);

      if (opts.wait) {
        info(`Polling job #${jobId} until completion...`);
        const interval = Number(opts.pollInterval);

        while (true) {
          const job = await indexer.getJob(jobId);
          const statusName = STATUS_NAMES[job.status] ?? String(job.status);

          info(`Status: ${statusName}`);

          // Terminal states: Completed(5), Disputed(6), Cancelled(7)
          if (job.status >= 5) {
            outputJobDetails(job);
            return;
          }

          await sleep(interval);
        }
      } else {
        const job = await indexer.getJob(jobId);
        outputJobDetails(job);
      }
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('accept')
  .description('Accept a job as provider')
  .argument('<jobId>', 'Job ID')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr) => {
    try {
      const client = getClient();
      const jobId = BigInt(jobIdStr);

      info('Fetching job details...');
      const job = await getJob(client, jobId);

      const txHash = await acceptJob(client, jobId, job.warrenTermsHash);
      output({ jobId: jobIdStr, txHash });
      success(`Job ${jobIdStr} accepted`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('deliver')
  .description('Submit a deliverable for a job')
  .argument('<jobId>', 'Job ID')
  .requiredOption('--hash <hex>', 'Deliverable hash (bytes32)')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr, opts) => {
    try {
      const client = getClient();
      const txHash = await submitDeliverable(client, BigInt(jobIdStr), opts.hash as Hex);
      output({ jobId: jobIdStr, txHash });
      success(`Deliverable submitted for job ${jobIdStr}`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('evaluate')
  .description('Evaluate a delivered job')
  .argument('<jobId>', 'Job ID')
  .option('--approve', 'Approve the deliverable', false)
  .option('--reject', 'Reject the deliverable', false)
  .option('--feedback <text>', 'Feedback text', '')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr, opts) => {
    try {
      if (!opts.approve && !opts.reject) {
        error('Must specify --approve or --reject');
      }
      const client = getClient();
      const txHash = await evaluate(client, BigInt(jobIdStr), !!opts.approve, opts.feedback);
      output({ jobId: jobIdStr, approved: !!opts.approve, txHash });
      success(`Job ${jobIdStr} evaluated: ${opts.approve ? 'approved' : 'rejected'}`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('settle')
  .description('Settle an evaluated job (release payment)')
  .argument('<jobId>', 'Job ID')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr) => {
    try {
      const client = getClient();
      const txHash = await settle(client, BigInt(jobIdStr));
      output({ jobId: jobIdStr, txHash });
      success(`Job ${jobIdStr} settled`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

jobCommand
  .command('cancel')
  .description('Cancel a job')
  .argument('<jobId>', 'Job ID')
  .option('--json', 'Output as JSON')
  .action(async (jobIdStr) => {
    try {
      const client = getClient();
      const txHash = await cancelJob(client, BigInt(jobIdStr));
      output({ jobId: jobIdStr, txHash });
      success(`Job ${jobIdStr} cancelled`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

function outputJobDetails(job: { jobId: number; offeringId: number; buyerAgentId: number; providerAgentId: number; priceUsdm: string; status: number; slaMinutes: number | null; createdAt: number | null; acceptedAt: number | null; deliveredAt: number | null; evaluatedAt: number | null; settledAt: number | null }) {
  output({
    jobId: job.jobId,
    offeringId: job.offeringId,
    buyerAgentId: job.buyerAgentId,
    providerAgentId: job.providerAgentId,
    price: formatUsdm(BigInt(job.priceUsdm)) + ' USDm',
    status: STATUS_NAMES[job.status] ?? String(job.status),
    slaMinutes: job.slaMinutes,
    createdAt: job.createdAt ? new Date(job.createdAt * 1000).toISOString() : null,
    acceptedAt: job.acceptedAt ? new Date(job.acceptedAt * 1000).toISOString() : null,
    deliveredAt: job.deliveredAt ? new Date(job.deliveredAt * 1000).toISOString() : null,
    evaluatedAt: job.evaluatedAt ? new Date(job.evaluatedAt * 1000).toISOString() : null,
    settledAt: job.settledAt ? new Date(job.settledAt * 1000).toISOString() : null,
  });
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

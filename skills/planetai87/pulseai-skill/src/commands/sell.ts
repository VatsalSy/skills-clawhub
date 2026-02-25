import { Command } from 'commander';
import {
  listOffering,
  getOffering,
  deactivateOffering,
  activateOffering,
  ServiceType,
  parseUsdm,
  formatUsdm,
  IndexerClient,
} from '@pulseai/sdk';
import { getClient, getReadClient } from '../config.js';
import { output, success, info, error, isJsonMode } from '../lib/output.js';

const SERVICE_TYPE_NAMES: Record<number, string> = {
  0: 'TextGeneration',
  1: 'ImageGeneration',
  2: 'DataAnalysis',
  3: 'CodeGeneration',
  4: 'Translation',
  5: 'Custom',
};

export const sellCommand = new Command('sell').description('Create and manage service offerings');

sellCommand
  .command('init')
  .description('Create a new service offering')
  .requiredOption('--agent-id <id>', 'Your agent ID')
  .requiredOption('--type <serviceType>', 'Service type (0-5 or name)')
  .requiredOption('--price <usdm>', 'Price in USDm (e.g. "5.0")')
  .requiredOption('--sla <minutes>', 'SLA in minutes')
  .requiredOption('--description <desc>', 'Offering description')
  .option('--schema-uri <uri>', 'Requirements schema URI')
  .option('--json', 'Output as JSON')
  .action(async (opts) => {
    try {
      const client = getClient();
      const serviceType = parseServiceType(opts.type);

      info(`Creating offering: ${opts.description}`);
      info(`Type: ${SERVICE_TYPE_NAMES[serviceType]} | Price: ${opts.price} USDm | SLA: ${opts.sla}m`);

      const result = await listOffering(client, {
        agentId: BigInt(opts.agentId),
        serviceType,
        priceUSDm: parseUsdm(opts.price),
        slaMinutes: Number(opts.sla),
        description: opts.description,
        requirementsSchemaURI: opts.schemaUri,
      });

      output({
        offeringId: result.offeringId,
        agentId: Number(opts.agentId),
        serviceType: SERVICE_TYPE_NAMES[serviceType],
        price: opts.price + ' USDm',
        slaMinutes: Number(opts.sla),
        description: opts.description,
        txHash: result.txHash,
      });
      success(`Offering created with ID: ${result.offeringId}`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

sellCommand
  .command('list')
  .description('List your offerings')
  .option('--agent-id <id>', 'Agent ID to list offerings for')
  .option('--json', 'Output as JSON')
  .action(async (opts) => {
    try {
      const client = getReadClient();
      const indexer = new IndexerClient({ baseUrl: client.indexerUrl });

      const filter = opts.agentId ? { agentId: Number(opts.agentId) } : {};
      const offerings = await indexer.getOfferings(filter);

      if (offerings.length === 0) {
        info('No offerings found.');
        if (isJsonMode()) output({ offerings: [], count: 0 });
        return;
      }

      if (isJsonMode()) {
        output({
          offerings: offerings.map((o) => ({
            offeringId: o.offeringId,
            agentId: o.agentId,
            serviceType: SERVICE_TYPE_NAMES[o.serviceType] ?? String(o.serviceType),
            priceUsdm: formatUsdm(BigInt(o.priceUsdm)),
            slaMinutes: o.slaMinutes,
            description: o.description,
            active: o.active,
          })),
          count: offerings.length,
        });
      } else {
        output(
          offerings.map((o) => ({
            id: o.offeringId,
            type: SERVICE_TYPE_NAMES[o.serviceType] ?? String(o.serviceType),
            price: formatUsdm(BigInt(o.priceUsdm)) + ' USDm',
            sla: o.slaMinutes ? `${o.slaMinutes}m` : '—',
            active: o.active ? 'yes' : 'no',
            description: o.description ?? '',
          })),
        );
      }
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

sellCommand
  .command('deactivate')
  .description('Deactivate an offering')
  .argument('<offeringId>', 'Offering ID')
  .option('--json', 'Output as JSON')
  .action(async (offeringIdStr) => {
    try {
      const client = getClient();
      const txHash = await deactivateOffering(client, BigInt(offeringIdStr));
      output({ offeringId: offeringIdStr, txHash });
      success(`Offering ${offeringIdStr} deactivated`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

sellCommand
  .command('activate')
  .description('Activate a deactivated offering')
  .argument('<offeringId>', 'Offering ID')
  .option('--json', 'Output as JSON')
  .action(async (offeringIdStr) => {
    try {
      const client = getClient();
      const txHash = await activateOffering(client, BigInt(offeringIdStr));
      output({ offeringId: offeringIdStr, txHash });
      success(`Offering ${offeringIdStr} activated`);
    } catch (e) {
      error(e instanceof Error ? e.message : String(e));
    }
  });

function parseServiceType(val: string): ServiceType {
  const num = Number(val);
  if (!isNaN(num) && num >= 0 && num <= 5) return num as ServiceType;
  const key = val as keyof typeof ServiceType;
  if (key in ServiceType) return ServiceType[key];
  throw new Error(
    `Invalid service type: ${val}. Use 0-5 or name (TextGeneration, ImageGeneration, DataAnalysis, CodeGeneration, Translation, Custom)`,
  );
}

#!/usr/bin/env python3
"""
RustChain Local x86 Miner - Modern Ryzen
"""
import os, sys, json, time, hashlib, uuid, requests, socket, subprocess, platform, statistics, re
from datetime import datetime

NODE_URL = "https://bulbous-bouffant.metalseed.net"
BLOCK_TIME = 600  # 10 minutes

class LocalMiner:
    def __init__(self, wallet=None):
        self.node_url = NODE_URL
        self.wallet = wallet or self._gen_wallet()
        self.hw_info = {}
        self.enrolled = False
        self.attestation_valid_until = 0
        self.last_entropy = {}

        print("="*70)
        print("RustChain Local Miner - Ryzen 5 5500")
        print("="*70)
        print(f"Node: {self.node_url}")
        print(f"Wallet: {self.wallet}")
        print("="*70)

    def _gen_wallet(self):
        data = f"ryzen5-{uuid.uuid4().hex}-{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:38] + "RTC"

    def _run_cmd(self, cmd):
        try:
            return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, timeout=10, shell=True).stdout.strip()
        except:
            return ""

    def _get_mac_addresses(self):
        """Return list of real MAC addresses present on the system."""
        macs = []
        # Try `ip -o link`
        try:
            output = subprocess.run(
                ["ip", "-o", "link"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=5,
            ).stdout.splitlines()
            for line in output:
                m = re.search(r"link/(?:ether|loopback)\s+([0-9a-f:]{17})", line, re.IGNORECASE)
                if m:
                    mac = m.group(1).lower()
                    if mac != "00:00:00:00:00:00":
                        macs.append(mac)
        except Exception:
            pass

        # Fallback to ifconfig
        if not macs:
            try:
                output = subprocess.run(
                    ["ifconfig", "-a"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=5,
                ).stdout.splitlines()
                for line in output:
                    m = re.search(r"(?:ether|HWaddr)\s+([0-9a-f:]{17})", line, re.IGNORECASE)
                    if m:
                        mac = m.group(1).lower()
                        if mac != "00:00:00:00:00:00":
                            macs.append(mac)
            except Exception:
                pass

        return macs or ["00:00:00:00:00:01"]

    def _collect_entropy(self, cycles: int = 48, inner_loop: int = 25000):
        """
        Collect simple timing entropy by measuring tight CPU loops.
        Returns summary statistics the node can score.
        """
        samples = []
        for _ in range(cycles):
            start = time.perf_counter_ns()
            acc = 0
            for j in range(inner_loop):
                acc ^= (j * 31) & 0xFFFFFFFF
            duration = time.perf_counter_ns() - start
            samples.append(duration)

        mean_ns = sum(samples) / len(samples)
        variance_ns = statistics.pvariance(samples) if len(samples) > 1 else 0.0

        return {
            "mean_ns": mean_ns,
            "variance_ns": variance_ns,
            "min_ns": min(samples),
            "max_ns": max(samples),
            "sample_count": len(samples),
            "samples_preview": samples[:12],
        }

    def _get_hw_info(self):
        """Collect hardware info"""
        hw = {
            "platform": platform.system(),
            "machine": platform.machine(),
            "hostname": socket.gethostname(),
            "family": "x86",
            "arch": "modern"  # Less than 10 years old
        }

        # Get CPU
        cpu = self._run_cmd("lscpu | grep 'Model name' | cut -d: -f2 | xargs")
        hw["cpu"] = cpu or "Unknown"

        # Get cores
        cores = self._run_cmd("nproc")
        hw["cores"] = int(cores) if cores else 6

        # Get memory
        mem = self._run_cmd("free -g | grep Mem | awk '{print $2}'")
        hw["memory_gb"] = int(mem) if mem else 32

        # Get MACs (ensures PoA signal uses real hardware data)
        macs = self._get_mac_addresses()
        hw["macs"] = macs
        hw["mac"] = macs[0]

        self.hw_info = hw
        return hw

    def attest(self):
        """Hardware attestation"""
        print(f"\n🔐 [{datetime.now().strftime('%H:%M:%S')}] Attesting...")

        self._get_hw_info()

        try:
            # Get challenge
            resp = requests.post(f"{self.node_url}/attest/challenge", json={}, timeout=10)
            if resp.status_code != 200:
                print(f"❌ Challenge failed: {resp.status_code}")
                return False

            challenge = resp.json()
            nonce = challenge.get("nonce")
            print(f"✅ Got challenge nonce")

        except Exception as e:
            print(f"❌ Challenge error: {e}")
            return False

        # Collect entropy just before signing the report
        entropy = self._collect_entropy()
        self.last_entropy = entropy

        # Submit attestation
        attestation = {
            "miner": self.wallet,
            "miner_id": f"ryzen5-{self.hw_info['hostname']}",
            "nonce": nonce,
            "report": {
                "nonce": nonce,
                "commitment": hashlib.sha256(
                    (nonce + self.wallet + json.dumps(entropy, sort_keys=True)).encode()
                ).hexdigest(),
                "derived": entropy,
                "entropy_score": entropy.get("variance_ns", 0.0)
            },
            "device": {
                "family": self.hw_info["family"],
                "arch": self.hw_info["arch"],
                "model": "AMD Ryzen 5 5500",
                "cpu": self.hw_info["cpu"],
                "cores": self.hw_info["cores"],
                "memory_gb": self.hw_info["memory_gb"]
            },
            "signals": {
                "macs": self.hw_info.get("macs", [self.hw_info["mac"]]),
                "hostname": self.hw_info["hostname"]
            }
        }

        try:
            resp = requests.post(f"{self.node_url}/attest/submit",
                               json=attestation, timeout=30)

            if resp.status_code == 200:
                result = resp.json()
                if result.get("ok"):
                    self.attestation_valid_until = time.time() + 580
                    print(f"✅ Attestation accepted!")
                    print(f"   CPU: {self.hw_info['cpu']}")
                    print(f"   Family: x86/modern")
                    print(f"   Expected Weight: 1.0x")
                    return True
                else:
                    print(f"❌ Rejected: {result}")
            else:
                print(f"❌ HTTP {resp.status_code}: {resp.text[:200]}")

        except Exception as e:
            print(f"❌ Error: {e}")

        return False

    def enroll(self):
        """Enroll in epoch"""
        if time.time() >= self.attestation_valid_until:
            print(f"📝 Attestation expired, re-attesting...")
            if not self.attest():
                return False

        print(f"\n📝 [{datetime.now().strftime('%H:%M:%S')}] Enrolling...")

        payload = {
            "miner_pubkey": self.wallet,
            "miner_id": f"ryzen5-{self.hw_info['hostname']}",
            "device": {
                "family": self.hw_info["family"],
                "arch": self.hw_info["arch"]
            }
        }

        try:
            resp = requests.post(f"{self.node_url}/epoch/enroll",
                                json=payload, timeout=30)

            if resp.status_code == 200:
                result = resp.json()
                if result.get("ok"):
                    self.enrolled = True
                    weight = result.get('weight', 1.0)
                    print(f"✅ Enrolled!")
                    print(f"   Epoch: {result.get('epoch')}")
                    print(f"   Weight: {weight}x")
                    return True
                else:
                    print(f"❌ Failed: {result}")
            else:
                error_data = resp.json() if resp.headers.get('content-type') == 'application/json' else {}
                print(f"❌ HTTP {resp.status_code}: {error_data.get('error', resp.text[:200])}")

        except Exception as e:
            print(f"❌ Error: {e}")

        return False

    def check_balance(self):
        """Check balance"""
        try:
            resp = requests.get(f"{self.node_url}/balance/{self.wallet}", timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                balance = result.get('balance_rtc', 0)
                print(f"\n💰 Balance: {balance} RTC")
                return balance
        except:
            pass
        return 0

    def mine(self):
        """Start mining"""
        print(f"\n⛏️  Starting mining...")
        print(f"Block time: {BLOCK_TIME//60} minutes")
        print(f"Press Ctrl+C to stop\n")

        # Save wallet
        with open("/tmp/local_miner_wallet.txt", "w") as f:
            f.write(self.wallet)
        print(f"💾 Wallet saved to: /tmp/local_miner_wallet.txt\n")

        cycle = 0

        try:
            while True:
                cycle += 1
                print(f"\n{'='*70}")
                print(f"Cycle #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*70}")

                if self.enroll():
                    print(f"⏳ Mining for {BLOCK_TIME//60} minutes...")

                    for i in range(BLOCK_TIME // 30):
                        time.sleep(30)
                        elapsed = (i + 1) * 30
                        remaining = BLOCK_TIME - elapsed
                        print(f"   ⏱️  {elapsed}s elapsed, {remaining}s remaining...")

                    self.check_balance()

                else:
                    print("❌ Enrollment failed. Retrying in 60s...")
                    time.sleep(60)

        except KeyboardInterrupt:
            print(f"\n\n⛔ Mining stopped")
            print(f"   Wallet: {self.wallet}")
            self.check_balance()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", help="Wallet address")
    args = parser.parse_args()

    miner = LocalMiner(wallet=args.wallet)
    miner.mine()

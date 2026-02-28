# CAN: Clock Address Naming

Name things. Find things. Verify things. Own agreements. CAN or NOT.

```
WHERE   hashspace    math names it        verified or NOT
WHEN    timespace    physics names it     stamped or NOT
WHAT    namespace    humans name it       claim as TRUE or NOT
```

## What

Every thing gets named three ways: by time (WHEN), by content hash (WHERE), and by human words (WHAT). Compute handles the first two automatically. Human edits the meaning. Both human and compute find agreement fast. Or NOT.

## Why

Paths lie. URLs break. DNS depends on ICANN. Cloud paths depend on a company existing next quarter. Content-addressing found the hash but lost the clock. Clock-addressing finds both: verify WHAT, prove WHEN, name freely.

CAN can not lie. The hash can't fake. The clock can't unsay. Physics doesn't negotiate.

CONTRACT agreements now. On logs, not just chains. LOG all things TRUE. And NOT.

## How

```bash
WHEN=$(date +%s%3N)
WHERE=$(sha256sum thing.txt | awk '{print $1}')
WHAT="thing.txt"
echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

One line. No npm. No pip. No runtime. No cloud. Works air-gapped. Works offline. Works on any machine with a clock and sha256.

## Find fast

Three legs to search. Know WHEN? Narrow by time. Know WHERE? Match the hash. Know WHAT? Search by name. Two legs narrow instantly. Three legs find exactly. Old naming had one leg: location. When it breaks you have zero legs.

## Falsify fast

Hash doesn't match? NOT. Instantly. No investigation, no committee, no appeal. The timer doesn't care.

## BAGS

```
HUSH    secret. never leaves scope. absolute.
GOOD    private. mine. my business.
FREN    trusted. signed. contract.
POST    public. by choice. by consent.
```

Default: HUSH. Everything else is opt-in.

## CAN three namespaces

```
DNS:        namespace only         (no verify, no time)
GIT:        hashspace only         (no time-first, no human name)
IPFS:       hashspace only         (dead snapshots, no clock)
BLOCKCHAIN: timespace + hashspace  (no human namespace)
CAN:        all three              (WHERE + WHEN + WHAT)
```

## Version

```
       ^ count up (features, tools, stacks, more and more)
1.8.0  CAN and NOT. Now what?
...
0.1.0  CAN NOT LIE. Root.
       v count down (less and less complex, more solid ground to build on)
```

CAN 0.1: if math and physics can lie, we're wrong. Until then, stack hash.

## References

Baran (1964), Diffie & Hellman (1976), Merkle (1979), Ostrom (1990), Zimmermann (1991), Szabo (1997), Grigg (2004), Torvalds (2005), Jacobson (2006), Day (2008), Nakamoto (2008), Taleb (2012), Crockford (JSON: version eternity).

## License

Public domain.

```
())) ← in the CAN
```

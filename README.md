# Veria Compliance Test

Automated verification tool for testing the [Veria Compliance API](https://veria.cc) against known OFAC-sanctioned wallet addresses.

## Overview

This script screens known sanctioned addresses through the Veria API to verify they are correctly identified as high-risk and blocked. Use this to:

- Verify your Veria integration is working correctly
- Test compliance screening in CI/CD pipelines  
- Demonstrate Veria's sanctions detection capabilities

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Veria-Protocol/veria-compliance-test.git
cd veria-compliance-test

# Install dependencies
pip install -r requirements.txt

# Run the test (uses sandbox mode without API key)
python test_sanctions.py
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API key (optional but recommended)

```bash
cp .env.example .env
# Edit .env and add your API key
```

Get your API key at [protocol.veria.cc](https://protocol.veria.cc)

### 3. Run the test

```bash
python test_sanctions.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `VERIA_API_URL` | API endpoint | `https://api.veria.cc/v1/screen` |
| `VERIA_API_KEY` | Your API key | None (sandbox mode) |

## API Response Format

The Veria `/v1/screen` endpoint returns:

```json
{
  "score": 95,
  "risk": "critical",
  "chain": "ethereum",
  "resolved": "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c",
  "latency_ms": 45,
  "details": {
    "sanctions_hit": true,
    "pep_hit": false,
    "watchlist_hit": true,
    "checked_lists": ["OFAC SDN", "UN Consolidated", "EU Sanctions", "UK HMT"],
    "address_type": "wallet"
  }
}
```

### Risk Levels

| Level | Score | Recommended Action |
|-------|-------|-------------------|
| low | 0-29 | Proceed |
| medium | 30-59 | Review |
| high | 60-79 | Block recommended |
| critical | 80-100 | Block required |

## Test Addresses

The script tests against known sanctioned addresses:

| Address | Authority |
|---------|----------|
| `0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c` | OFAC (Tornado Cash) |
| `0xd90e2f925da726b50c4ed8d0fb90ad053324f31b` | OFAC |
| `0x7ff9cfad3877f21d41a833ed410082199f751303` | Lazarus Group |

## Expected Output

```
🛡️  Starting Veria Compliance Verification...
   Target: https://api.veria.cc/v1/screen
   Mode: Live API
   API Key: Configured
   Testing 3 known sanctioned entities.

------------------------------------------------------------
🔎 Screening: 0x8576acc5c0... ✅ [BLOCKED] Score: 95, Risk: critical, Sanctions: True
🔎 Screening: 0xd90e2f925d... ✅ [BLOCKED] Score: 95, Risk: critical, Sanctions: True
🔎 Screening: 0x7ff9cfad38... ✅ [BLOCKED] Score: 95, Risk: critical, Sanctions: True
------------------------------------------------------------

Results: 3/3 threats caught

✅ Summary: Veria API correctly identifies all OFAC-listed addresses.
```

## Mock Mode

For demos without hitting the live API, edit `test_sanctions.py` and set:

```python
use_mock = True
```

## Integration Example

```python
import requests

def screen_wallet(address: str, api_key: str) -> dict:
    """Screen a wallet address for compliance risks."""
    response = requests.post(
        "https://api.veria.cc/v1/screen",
        json={"input": address},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    return response.json()

# Usage
result = screen_wallet("0x742d35Cc6634C0532925a3b844Bc454e4438f44e", "veria_live_xxx")
if result["risk"] in ["high", "critical"] or result["details"]["sanctions_hit"]:
    print("Transaction blocked for compliance")
```

## Resources

- [Veria Documentation](https://docs.veria.cc)
- [API Reference](https://docs.veria.cc/api)
- [Get API Key](https://protocol.veria.cc)

## License

MIT License - See [LICENSE](LICENSE) file for details.

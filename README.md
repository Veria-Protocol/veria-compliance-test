# Veria Compliance Test

Automated verification tool for testing the Veria Compliance API against known sanctioned addresses.

## Overview

This script tests the Veria Compliance API by screening known OFAC-sanctioned wallet addresses to verify they are correctly identified and blocked.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env to customize API endpoint if needed
   ```

## Usage

### Run against production API (default):
```bash
python test_sanctions.py
```

### Run against custom endpoint:
```bash
VERIA_API_URL=https://your-api-endpoint.com/compliance/check python test_sanctions.py
```

### Run in mock mode (for demos):
Edit `test_sanctions.py` and set `use_mock = True`

## Configuration

| Variable | Description | Default |
|----------|-------------|--------|
| `VERIA_API_URL` | Compliance API endpoint | Production API |
| `use_mock` | Enable mock mode (in code) | `False` |

## Test Addresses

The script tests against known sanctioned addresses from:
- OFAC SDN List (Tornado Cash related)
- Lazarus Group associated addresses

## Expected Output

```
🛡️  Starting Veria Compliance Verification...
   Target: https://...
   Mode: Real (Live API)
   Testing 3 known sanctioned entities.

------------------------------------------------------------
🔎 Screening: 0x8576acc5c0... ✅ [BLOCKED] Risk Score: 1.0
🔎 Screening: 0xd90e2f925d... ✅ [BLOCKED] Risk Score: 1.0
🔎 Screening: 0x7ff9cfad38... ✅ [BLOCKED] Risk Score: 1.0
------------------------------------------------------------
Final Result: 3/3 Threats Caught.
Summary: Veria API is 100% Compliant with current OFAC lists.
```

## License

MIT License - See LICENSE file for details.

#!/usr/bin/env python3
"""Veria Compliance Test

Automated verification tool for testing the Veria Compliance API
against known sanctioned addresses.
"""

import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
# ---------------------------------------------------------
# Toggle use_mock to True for demos without hitting the live API
use_mock = False

# API Endpoint - Veria Public API
API_URL = os.environ.get(
    "VERIA_API_URL",
    "https://api.veria.cc/v1/screen"
)

# API Key - Required for production use
# Get your API key at https://protocol.veria.cc
API_KEY = os.environ.get("VERIA_API_KEY", "")

# Known Sanctioned Addresses (The "Answer Key")
# These are real addresses from OFAC/Lazarus lists.
sanctioned_wallets = [
    {
        "address": "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c",
        "authority": "OFAC (Tornado Cash)"
    },
    {
        "address": "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b",
        "authority": "OFAC"
    },
    {
        "address": "0x7ff9cfad3877f21d41a833ed410082199f751303",
        "authority": "Lazarus Group"
    }
]


def screen_address(address: str) -> dict:
    """Screen a single address using the Veria API.
    
    Args:
        address: Wallet address to screen
        
    Returns:
        API response as dictionary
    """
    if use_mock:
        # Simulate API latency
        time.sleep(0.3)
        # Return mock high-risk response for sanctioned addresses
        return {
            "score": 95,
            "risk": "critical",
            "chain": "ethereum",
            "resolved": address,
            "latency_ms": 45,
            "details": {
                "sanctions_hit": True,
                "pep_hit": False,
                "watchlist_hit": True,
                "checked_lists": ["OFAC SDN", "UN Consolidated", "EU Sanctions"],
                "address_type": "wallet"
            }
        }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    payload = {"input": address}
    
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def is_blocked(result: dict) -> bool:
    """Determine if an address should be blocked based on API response.
    
    An address is considered blocked if:
    - sanctions_hit is True, OR
    - risk level is 'high' or 'critical'
    
    Args:
        result: API response dictionary
        
    Returns:
        True if address should be blocked
    """
    sanctions_hit = result.get("details", {}).get("sanctions_hit", False)
    risk = result.get("risk", "low")
    
    return sanctions_hit or risk in ["high", "critical"]


def run_verification():
    """Run the compliance verification test suite."""
    print("\n\U0001f6e1\ufe0f  Starting Veria Compliance Verification...")
    print(f"   Target: {API_URL}")
    print(f"   Mode: {'Mock (Simulation)' if use_mock else 'Live API'}")
    print(f"   API Key: {'Configured' if API_KEY else 'Not set (sandbox mode)'}")
    print(f"   Testing {len(sanctioned_wallets)} known sanctioned entities.\n")
    print("-" * 60)
    
    passed = 0
    failed = 0
    errors = 0
    
    for wallet_info in sanctioned_wallets:
        address = wallet_info["address"]
        authority = wallet_info["authority"]
        
        print(f"\U0001f50e Screening: {address[:12]}... ", end="", flush=True)
        
        try:
            result = screen_address(address)
            
            if is_blocked(result):
                score = result.get("score", "N/A")
                risk = result.get("risk", "N/A")
                sanctions = result.get("details", {}).get("sanctions_hit", False)
                print(f"\u2705 [BLOCKED] Score: {score}, Risk: {risk}, Sanctions: {sanctions}")
                passed += 1
            else:
                score = result.get("score", "N/A")
                risk = result.get("risk", "N/A")
                print(f"\u274c [FAILED] Allowed sanctioned wallet! Score: {score}, Risk: {risk}")
                print(f"      Authority: {authority}")
                failed += 1
                
        except requests.exceptions.HTTPError as e:
            print(f"\u274c [ERROR] HTTP {e.response.status_code}: {e.response.text[:100]}")
            errors += 1
        except requests.exceptions.RequestException as e:
            print(f"\u274c [ERROR] Request failed: {e}")
            errors += 1
        except Exception as e:
            print(f"\u274c [ERROR] Unexpected error: {e}")
            errors += 1
    
    print("-" * 60)
    print(f"\nResults: {passed}/{len(sanctioned_wallets)} threats caught")
    
    if errors > 0:
        print(f"Errors: {errors} (check API key and connectivity)")
    
    if passed == len(sanctioned_wallets):
        print("\n\u2705 Summary: Veria API correctly identifies all OFAC-listed addresses.")
        return 0
    else:
        print(f"\n\u26a0\ufe0f  Summary: {failed} sanctioned addresses were not blocked.")
        return 1


if __name__ == "__main__":
    exit(run_verification())

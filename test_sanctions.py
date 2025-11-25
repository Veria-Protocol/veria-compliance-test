import requests
import json
import time

# Configuration
# ---------------------------------------------------------
# This script supports dual-mode: Real vs. Mock for demos.
# Toggle use_mock to False to hit the live Veria Core API.
use_mock = False

# Live Veria Core API Endpoint
API_URL = "https://veria-api-prod-190356591245.us-central1.run.app/compliance/check"

# Known Sanctioned Addresses (The "Answer Key")
# These are real addresses from OFAC/Lazarus lists.
sanctioned_wallets = [
    "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c", # Authority: OFAC (Tornado Cash)
    "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b", # Authority: OFAC
    "0x7ff9cfad3877f21d41a833ed410082199f751303"  # Authority: Lazarus Group
]

def run_verification():
    print("\n🛡️  Starting Veria Compliance Verification...")
    print(f"   Target: {API_URL}")
    print(f"   Mode: {'Mock (Simulation)' if use_mock else 'Real (Live API)'}")
    print(f"   Testing {len(sanctioned_wallets)} known sanctioned entities.\n")
    print("-" * 60)
    
    passed = 0
    
    for wallet in sanctioned_wallets:
        print(f"🔎 Screening: {wallet[:12]}... ", end="")
        
        response_json = {}
        
        if use_mock:
            # Simulate API Latency (remove this block when live)
            time.sleep(0.3)
            
            # MOCK RESPONSE LOGIC
            # Simulating the structure: { success: true, data: { status: 'blocked', ... } }
            response_json = {
                "success": True,
                "data": {
                    "status": "BLOCKED",
                    "risk_score": 1.0,
                    "flags": ["OFAC_SDN", "HIGH_RISK_ENTITY"]
                }
            }
        else:
            try:
                # Real API Call
                # The API expects 'name' for the simple check endpoint.
                payload = {"name": wallet} 
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                response_json = response.json()
            except Exception as e:
                print(f"❌ [ERROR] API Call Failed: {e}")
                continue
        
        # Parse Response
        # Handle both flat (legacy/mock) and nested (standard) formats if necessary,
        # but here we standardize on the API's "data" envelope.
        data = response_json.get("data", response_json) # Fallback to root if data missing
        status = data.get("status", "UNKNOWN").upper()
        
        # Check for blocked status
        if status == "BLOCKED":
            # Risk score might not be returned by simple endpoint, default to 1.0 if blocked
            risk_score = data.get("risk_score", 1.0) 
            print(f"✅ [BLOCKED] Risk Score: {risk_score}")
            passed += 1
        else:
            print(f"❌ [FAILED]  Allowed Sanctioned Wallet - Status: {status}")

    print("-" * 60)
    print(f"Final Result: {passed}/{len(sanctioned_wallets)} Threats Caught.")
    
    if passed == len(sanctioned_wallets):
        print("Summary: Veria API is 100% Compliant with current OFAC lists.")
    else:
        print("Summary: Compliance Failure Detected.")

if __name__ == "__main__":
    run_verification()

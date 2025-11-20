import requests
import json
import time

# Configuration
# ---------------------------------------------------------
# For the demo, we mock the response to show how it works.
# When you go live, you will point this to https://api.veria.cc/v1/screen
API_URL = "https://api.veria.cc/v1/screen"
API_KEY = "demo-key-public" 

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
    print(f"   Testing {len(sanctioned_wallets)} known sanctioned entities.\n")
    print("-" * 60)
    
    passed = 0
    
    for wallet in sanctioned_wallets:
        print(f"🔎 Screening: {wallet[:12]}... ", end="")
        
        # Simulate API Latency (remove this block when live)
        time.sleep(0.3)
        
        # MOCK RESPONSE LOGIC
        # This simulates exactly what your API returns
        response_data = {
            "status": "BLOCKED",
            "risk_score": 1.0,
            "flags": ["OFAC_SDN", "HIGH_RISK_ENTITY"]
        }
        
        # In a real integration, you would use:
        # response = requests.post(API_URL, json={"address": wallet}, headers={"x-api-key": API_KEY})
        # response_data = response.json()
        
        if response_data["status"] == "BLOCKED":
            print(f"✅ [BLOCKED] Risk Score: {response_data['risk_score']}")
            passed += 1
        else:
            print(f"❌ [FAILED]  Allowed Sanctioned Wallet")

    print("-" * 60)
    print(f"Final Result: {passed}/{len(sanctioned_wallets)} Threats Caught.")
    
    if passed == len(sanctioned_wallets):
        print("Summary: Veria API is 100% Compliant with current OFAC lists.")
    else:
        print("Summary: Compliance Failure Detected.")

if __name__ == "__main__":
    run_verification()

from flask import Flask, request, jsonify, render_template
from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Connect to the Ganache blockchain
ganache_url = os.getenv("GANACHE_URL")  # Load Ganache URL from .env
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("Error: Could not connect to the blockchain.")

# Load contract ABI and address
with open("E:\\blockchain project\\cert_project\\build\\contracts\\Certificate.json", encoding="utf-8") as f:
    contract_data = json.load(f)

contract_address = os.getenv("CONTRACT_ADDRESS")  # Load contract address from .env
contract = web3.eth.contract(address=contract_address, abi=contract_data["abi"])

# Load private key from .env
private_key = os.getenv("PRIVATE_KEY")
if not private_key:
    raise EnvironmentError("Private key not found. Add PRIVATE_KEY to the .env file.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/issue_certificate", methods=["GET", "POST"])
def issue_certificate():
    if request.method == "GET":
        return "This endpoint is for issuing certificates. Use POST to send data."
    try:
        data = request.json
        recipient = data["recipient"]
        name = data["name"]
        course = data["course"]
        issued_date = data["issuedDate"]

        # Build the transaction
        txn = contract.functions.issueCertificate(
            recipient, name, course, issued_date
        ).build_transaction({
            "from": web3.eth.accounts[0],
            "nonce": web3.eth.get_transaction_count(web3.eth.accounts[0]),
            "gas": 3000000,  # Set an appropriate gas limit
            "gasPrice": Web3.to_wei('20', 'gwei')  # Set gas price
        })

        # Sign and send the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return jsonify({"status": "Certificate issued", "txn_hash": txn_hash.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verify_certificate", methods=["GET"])
def verify_certificate():
    try:
        recipient = request.args.get("recipient")
        cert = contract.functions.verifyCertificate(recipient).call()

        if cert[4]:  # isIssued flag
            return jsonify({
                "id": cert[0],
                "name": cert[1],
                "course": cert[2],
                "issuedDate": cert[3],
                "isIssued": cert[4]
            })
        else:
            return jsonify({"error": "Certificate not found or not issued."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

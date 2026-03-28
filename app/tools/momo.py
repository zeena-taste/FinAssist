def initiate_momo_payment(params: dict) -> dict:
    """Simulate a mobile money transfer."""
    amount = params.get('amount', 0)
    recipient = params.get('recipient', 'unknown')
    print(f"[MOMO TOOL] Transferring {amount} to {recipient}")
    return {"status": "success", "message": f"Successfully transferred {amount} to {recipient}"}

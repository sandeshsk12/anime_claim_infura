import asyncio
import websockets
import json

async def subscribe():
    uri = "wss://arbitrum-mainnet.infura.io/ws/v3/xx"  # Replace with your Infura API Key
    
    # Payload to subscribe to new block headers
    subscription_message = {

        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["logs", {"address": "0xecC4C9e7Bc93CAb46DbA99B4b85cC82D3cFbAE86", "topics":["0x9fb8cf0df5a043b3003ee5402e773eca3296ff3e0af8aa116ac898a017bdb2e4"]}]
    }
    
    # Open a WebSocket connection to the Infura endpoint
    async with websockets.connect(uri) as websocket:
        # Send the subscription message
        await websocket.send(json.dumps(subscription_message))
        print(f"Sent subscription request: {json.dumps(subscription_message)}")

        # Continuously listen for new messages
        while True:
            response = await websocket.recv()
                        # Convert the JSON string to a Python dictionary
            response_dict = json.loads(response)
            # print(response_dict)

            # Now, try to access the correct structure
            if 'params' in response_dict and 'result' in response_dict['params']:
                # Accessing 'number' from the 'result' key

                amount_claimed_hex = response_dict['params']['result']['data']
                amount_claimed_hex = amount_claimed_hex[66:]
                amount_claimed_hex = int(amount_claimed_hex, 16)
                print(f"Amount claimed: {amount_claimed_hex}")
            else:
                print("The expected keys are missing in the response!")



    

# Run the asynchronous function
asyncio.get_event_loop().run_until_complete(subscribe())


# wscat -c wss://mainnet.infura.io/ws/v3/<YOUR-API-KEY> -x '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["logs", {"address": "0x8320fe7702b96808f7bbc0d4a888ed1468216cfd", "topics":["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"]}]}'

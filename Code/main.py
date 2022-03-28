import asyncio
import os
import sys
from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient

from device_provisioning_service import Device
from Sensors.SensorPoller import SensorPoller



async def main():
    scopeID = None
    deviceId = None
    key = None

    load_dotenv() # Loads the .env file into the environment
    scopeID = os.getenv('SCOPE_ID') # Get the scope ID from the environment
    deviceId = os.getenv('DEVICE_ID') # Get the device ID from the environment
    key = os.getenv('DEVICE_KEY') # Get the device key from the environment
    
    if scopeID is None or deviceId is None or key is None:
        sys.exit(1)

    dps = Device(scopeID, deviceId, key) # Create a Device Provisioning Service object

    conn_str = await dps.connection_string # Get the connection string from the Device Provisioning Service

    # Connect to the IoT Hub
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()
    

    # Get the data from the sensors
    data = SensorPoller().poll_sensors() 

    try:
        while(1):
            await device_client.send_message(data) # Send the data to the IoT Hub
            await asyncio.sleep(60) # Sleep for 60 seconds
    except:
        print("Unexpected error:", sys.exc_info()[0])

    await device_client.disconnect() # Disconnect from the IoT Hub


if __name__ == "__main__":
    asyncio.run(main())

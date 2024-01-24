from azure.iot.device import IoTHubDeviceClient
import Mqtt_Tag as mt








# define behavior for receiving a message
def message_handler(message):
    global tag
    print("the data in the message received was ")
    print(message.data.decode('utf-8'))
    print("data type")
    print(type(message.data))
    print("custom properties are")
    print(message.custom_properties)
    tag.CallProductCode(message.data.decode('utf-8'))
    





# # Wait for user to indicate they are done listening for messages
# while True:
#     selection = input("Press Q to quit\n")
#     if selection == "Q" or selection == "q":
#         print("Quitting...")
#         break





if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    try:
        conn_str="HostName=sankyo-iothub.azure-devices.net;DeviceId=EPC1522-1;SharedAccessKey=F1vN5o544+iWHRyxkspeuyHoU9TgCsp1vAIoTOSixco="
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        # connect the client.
        device_client.connect()

        # set the message handler on the client
        device_client.on_message_received = message_handler

        global tag 
        # tag = mt.Mqtt_Tag("mqtt-tag-server", 1883)
        tag = mt.Mqtt_Tag("axcf3152", 51883)
        tag.Mqtt_start()
        while True:
            tag.CallProductCode(str(input("Enter ProductCode")))
    except:
        print("Program End Now")
        device_client.shutdown()

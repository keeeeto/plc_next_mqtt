#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from time import sleep


class Mqtt_Tag:

    productlist = []
    flag = 0

    def __init__(self, adress, port):
        self.broker_adress = adress
        self.port = port

    def on_connect(self, client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # show connection state
        client.subscribe("mqtt_tag/#")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def on_publish(self, client, userdata, mid):
        print("publish: {0}".format(mid))

    def on_message(self, client, userdata, msg):

        self.RegisterProductCode(msg)
        self.CheckFinishTag(msg)

    def Mqtt_start(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message

        self.client.connect(self.broker_adress, self.port)

        self.client.loop_start()

    def CallProductCode(self, product_code):  # product_code is str
        self.client.publish("mqtt_tag/buzzer_code", product_code)
        self.flag = 1  # on call

    def RegisterProductCode(self, msg):
        if ("mqtt_tag/alive/" in msg.topic):
            topic_name = msg.topic.replace("mqtt_tag/alive/", '')
            if (len(self.productlist) == 0):
                if (topic_name not in self.productlist):
                    self.productlist.append([topic_name, msg.payload])
                    print(self.productlist)
            else:
                in_flag = True
                for i in range(len(self.productlist)):
                    # print(i)
                    # print(topic_name in self.productlist[i])
                    if (topic_name in self.productlist[i]):
                        in_flag = False
                        break
                if (in_flag):
                    self.productlist.append([topic_name, msg.payload])
                    print(self.productlist)
                else:
                    for i in range(len(self.productlist)):
                        if (topic_name in self.productlist[i]):
                            self.productlist[i][1] = msg.payload
                            break
            # print(self.productlist)

    def CheckFinishTag(self, msg):
        if ("mqtt_tag/finish_tag" in msg.topic):
            self.CallProductCode("")
            self.flag = 0  # end call event

    def GetCallState(self):
        return self.flag

    def SetCallState(self, flag):
        self.flag = flag


if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    # tag = Mqtt_Tag("mqtt-tag-server", 1883)
    tag = Mqtt_Tag("192.168.10.2", 51883)
    tag.Mqtt_start()
    # tag.CallProductCode("255")
    while True:
        # tag.CallProductCode("255")
        # sleep(1)

        tag.CallProductCode(str(input("Enter ProductCode")))

        # plist = [["255", 5], ["244", 6]]
        # print("255" in plist[0])
        sleep(1)

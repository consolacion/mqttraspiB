#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import package
import paho.mqtt.client as mqtt
#add for output
import RPi.GPIO as GPIO
import socket

# Define Variables
MQTT_HOST = "192.168.1.103"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "raspiB/pin18"
#
LED1 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT)
try:
  # Define on connect event function
  # Subscribe to Topic in this function
  def on_connect(self,mosq, obj, rc):
     mqttc.subscribe(MQTT_TOPIC, 0)
     print("Connect on "+MQTT_HOST)
     mqttc.publish(MQTT_TOPIC+"/alive","alive")
     mqttc.publish(MQTT_TOPIC+"/IP",get_ip())
     mqttc.publish(MQTT_TOPIC+"/name","mqttpin18.py")
  # Define on_message event function. 
  # This function will be invoked every time,
  # a new message arrives for the subscribed topic 
  def on_message(mosq, obj, msg):
     if (msg.payload=='ON'):
           GPIO.output(LED1,True)
           print 'lamp aan'
           print "Topic: " + str(msg.topic)
           print "QoS: " + str(msg.qos)
           mqttc.publish(MQTT_TOPIC+"/state","ON")
     if (msg.payload=='OFF'):
           GPIO.output(LED1,False)
           print 'lamp uit'
           print "Topic: " + str(msg.topic)
           print "QoS: " + str(msg.qos)
           mqttc.publish(MQTT_TOPIC+"/state","OFF")

  def on_subscribe(mosq, obj, mid, granted_qos):
          print("Subscribed to Topic: " + 
          MQTT_TOPIC + " with QoS: " + str(granted_qos))


  def get_ip():
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      try:
          # doesn't even have to be reachable
          s.connect(('10.255.255.255', 1))
          IP = s.getsockname()[0]
      except:
          IP = '127.0.0.1'
      finally:
          s.close()
      return IP
  print(get_ip())


    # Initiate MQTT Client
  mqttc = mqtt.Client()

    # Assign event callbacks
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_subscribe = on_subscribe

    # Connect with MQTT Broker
  mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Continue monitoring the incoming messages for subscribed topic
  mqttc.loop_forever()

except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C
    mqttc.publish(MQTT_TOPIC+"/state","OFF")
    GPIO.cleanup()  
#finally:  
    #GPIO.cleanup() # this ensures a clean exit  


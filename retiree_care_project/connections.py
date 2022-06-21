import ftplib
import paho.mqtt.client as mqtt
from .ftpOwn import FtpOwn


'''MQTT CONNECTION'''
def mqtt_connection():
    client = mqtt.Client()
    client.username_pw_set("tomatocoder", "Coder_tomato1")
    client.connect("mqtt.pi40.ru", 1883)
    client.subscribe("tomatocoder/go")
    return client

'''FTP CONNECTION'''
def ftp_connection():
    try:
        ftp = FtpOwn()
        ftp.ftpConnect("213.226.112.19", 21)
        return ftp
    except ftplib.error_perm as e:
        print(e)
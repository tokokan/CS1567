#!/usr/bin/env python

import rospy
import math
from cmvision.msg import Blobs, Blob
from geometry_msgs.msg import Twist


def blobsCallback(data):
        global pub
        command = Twist()
        x= 0
        y= 0
        area = 0
        
        command.angular.z = 0
        command.linear.x = 0
        if data.blob_count > 0:
                for box in data.blobs:
                        area = area + box.area
                        x = x + (box.x * box.area)
                        y = y + (box.y * box.area)
                if area != 0:                
                        x = x / area
                        y = y / area

                if (area > 7000):
                        command.linear.x = 0.2
                elif (area < 4000):
                        command.linear.x = -0.2

                if(x < (data.image_width / 2.3)):
                        command.angular.z = 1                       
                elif(x > data.image_width / 1.7):
                        command.angular.z = -1
        pub.publish(command)
                        
        print "(%i, %i, %i)" % (x, y, area)
        
      

def detect_blob():
        global pub
        rospy.init_node('blob_tracker', anonymous = True)
        rospy.Subscriber('/blobs', Blobs, blobsCallback)
        pub = rospy.Publisher('kobuki_command', Twist, queue_size = 10)
        rospy.spin()


if __name__ == '__main__':
        detect_blob()

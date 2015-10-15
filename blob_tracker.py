#!/usr/bin/env python

import rospy
import math
from cmvision.msg import Blobs, Blob
from geometry_msgs.msg import Twist

lastError = 0.0
state = 0
odomDist
odomDegree
odomPub
theta1
theta2
theta3
theta4
theta5
xS

def blobsCallback(data):
        global pub, state, lastError, odomPub, odomDegree, odomDist, theta1, theta2, theta3, theta4, theta5, xS
        
        command = Twist()
        x= 0
        y= 0
        area = 0
        
        command.angular.z = 0
        command.linear.x = 0
        if state == 0 && data.blob_count > 0:
                for box in data.blobs:
                        if box.name == 'Green':
                                area = area + box.area
                                x = x + (box.x * box.area)
                                y = y + (box.y * box.area)
                                if area != 0:                
                                        x = x / area
                                        y = y / area

                if area == 0:
                        odomPub.publish(Empty())
                        command.linear.x = 0
                        state = 1
                        raw_input('Please pull the lid up')
                        state = 2
                else:
                        command.linear.x = 0.2
                #if (area > 7000):
                #        command.linear.x = 0.2
                #elif (area < 4000):
                #        command.linear.x = -0.2
                #
                        error = ( data.image_width/2.0 - x) / (data.image_width/2.0)
                        KP = 2
                        derivative = 0.0
                        KD = .5
                
                        derivative = error-lastError
                        #if error < 0 :
                        #        derivative = -derivative

                        if (  (data.image_width / 2.3) < x < (data.image_width / 1.7) ):
                                command.angular.z = 0
                        else:
                                command.angular.z= error*KP + KD*derivative
                #elif(x < (data.image_width / 2.3)):
                #        command.angular.z = 1                       
                #elif(x > data.image_width / 1.7):
                 #       command.angular.z = -1
                        lastError = error
        elif state == 2:
                for box in data.blobs:
                        if box.name == 'Orange':
                                area = area + box.area
                                x = x + (box.x * box.area)
                                y = y + (box.y * box.area)
                                if area != 0:                
                                        x = x / area
                                        y = y / area
                        if area != 0:
                                error = ( data.image_width/2.0 - x) / (data.image_width/2.0)
                                if (  (data.image_width / 2.3) < x < (data.image_width / 1.7) ):
                                        command.angular.z = 0
                                        theta1 = odomDegree
                                        state = 3
                                else:
                                        command.angular.z= error*2.0
                        else:
                                command.angular.z = 1
        elif state == 3:
             for box in data.blobs:
                        if box.name == 'Red':
                                area = area + box.area
                                x = x + (box.x * box.area)
                                y = y + (box.y * box.area)
                                if area != 0:                
                                        x = x / area
                                        y = y / area 
                        if area != 0:
                                error = ( data.image_width/2.0 - x) / (data.image_width/2.0)
                                if (  (data.image_width / 2.3) < x < (data.image_width / 1.7) ):
                                        command.angular.z = 0
                                        theta2 = odomDegree
                                        state = 4
                                else:
                                        command.angular.z= error*2.0
                        else:
                                command.angular.z = 1                          
        elif state == 4:
                if theta2 > 0:
                        error = odomDegree - 90
                        command.angular.z = -error/20
                        if error == 0:
                                state = 5
                                odomPub.publish(Empty())
                elif theta2 <= 0:
                        error = odomDegree + 90
                        command.angular.z = -error/20
                        if error == 0:
                                state = 5
                                odomPub.publish(Empty())
        elif state == 5:
                error = .3 - odomDist
                command.linear.x = error
                if error == 0
                        state = 6
                        odomPub.publish(Empty())
        elif state == 6:
                for box in data.blobs:
                        if box.name == 'Orange':
                                area = area + box.area
                                x = x + (box.x * box.area)
                                y = y + (box.y * box.area)
                                if area != 0:                
                                        x = x / area
                                        y = y / area
                        if area != 0:
                                error = ( data.image_width/2.0 - x) / (data.image_width/2.0)
                                if (  (data.image_width / 2.3) < x < (data.image_width / 1.7) ):
                                        command.angular.z = 0
                                        theta3 = odomDegree
                                        state = 7
                                else:
                                        command.angular.z= error*2.0
                        else:
                                command.angular.z = 1
        elif state == 7:        
                for box in data.blobs:
                        if box.name == 'Red':
                                area = area + box.area
                                x = x + (box.x * box.area)
                                y = y + (box.y * box.area)
                                if area != 0:                
                                        x = x / area
                                        y = y / area
                        if area != 0:
                                error = ( data.image_width/2.0 - x) / (data.image_width/2.0)
                                if (  (data.image_width / 2.3) < x < (data.image_width / 1.7) ):
                                        command.angular.z = 0
                                        theta4 = odomDegree
                                        state = 8
                                else:
                                        command.angular.z= error*2.0
                        else:
                                command.angular.z = 1
        elif state == 8:
                temptheta1 = 90 - fabs(theta1)
                temptheta2 = 90 - fabs(theta2)
                yG = .3 * tan(temptheta1) * tan(theta3)/(tan(theta3) - tan(temptheta1))
                xB = .3 + .3 * tan(temptheta2) / (tan(theta4) - tan(temptheta2))
                xG = .3 + .3 * tan(theta1) / (tan(theta3) - tan(theta1))
                yB = .3 * tan(temptheta2) * tan(theta4) / (tan(theta4) - tan(temptheta2))
                
                m = (yG - yB)/(xG - xB)
                b = yG - M * xG

                xS = -b / M
                theta5 = atan(yG/(fabs(xS - .3 - .3 * tan(temptheta1)/(tan(theta3) - tan(temptheta1)))))
                
                state = 9;

        elif state == 9:
                error = xS - .3 - odomDist
                command.linear.x = error
                if error == 0
                        state = 10
                        odomPub.publish(Empty())
        elif state == 10:
                if (theta1 > 0  && xS - .3 > 0):
                        error = odomDegree + (180 - theta5)
                        command.angular.z = -error/20
                elif (theta1 > 0 && xS - .3 <= 0):
                        error = odomDegree + theta5
                        command.angular.z = -error/20
                elif (theta1 < 0 && xS - .3 > 0):
                        error = (180 - theta5) - odomDegree
                        command.angular.z = error/20
                elif (theta1 < 0 && xS - .3 <= 0):
                        error = theta5 - odomDegree
                        command.angular.z = error/20
                
                if error == 0:
                        state == 11
                        odomPub.publish(Empty())
        elif state == 11:
                command.linear.x = .2               
                if odomDist == yB / cos(theta5) + .05:
                        command.linear.x = 0
                        state = 1
        
        pub.publish(command)
                
        
        print "(%i, %i, %i)" % (x, y, area)
        
def odomCallback(data)
        global odomDegree
        global odomDist
        q = [data.pose.pose.orientation.x,
         data.pose.pose.orientation.y,
         data.pose.pose.orientation.z,
         data.pose.pose.orientation.w]
	roll, pitch, yaw = euler_from_quaternion(q)
    	odomDegree = yaw * 180 / math.pi
        odomDist = data.pose.pose.position.x      

def detect_blob():
        global pub
        rospy.init_node('blob_tracker', anonymous = True)
        rospy.Subscriber('/blobs', Blobs, blobsCallback)
        rospy.Subscriber('/odom', Odometry, odomCallback)
        odomPub = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)  
        pub = rospy.Publisher('kobuki_command', Twist, queue_size = 10)
        rospy.spin()


if __name__ == '__main__':
        detect_blob()

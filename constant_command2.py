#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

##################################
'''
everything should now be working as outlined in the lab sheet!
the trouble was actually in remote_control: all I did was add a loop to continue prompting the user for commands until shutdown.  I guess the node was terminating right after the stop command was sent, which cancelled the command? Whatever it was, it's fixed now, and we know that constant_command2 is/was OK, which is the important part.
'''
################################## 

command = Twist()
command.linear.x = 0.0
command.angular.z = 0.0

def messengerCallback(data):
    #global pub
    #global command
    print "got new command!"
    command.linear.x = data.linear.x
    command.angular.z = data.angular.z
    command.linear.z = data.linear.z
    print "the command is:"
    print command.linear.x , command.angular.z, command.linear.z



def send_commands():
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    rospy.Subscriber("kobuki_command",Twist,messengerCallback, queue_size = 10)
    rospy.init_node('constant_command', anonymous=True)
    rate = rospy.Rate(1)
    while pub.get_num_connections() == 0:
        pass
    while not rospy.is_shutdown():
    	pub.publish(command)
	print "publishing " ,command.linear.x, command.angular.z, command.linear.z
    	rospy.sleep(.1)

if __name__ == '__main__':
    try:
        send_commands()
    except rospy.ROSInterruptException:
        pass


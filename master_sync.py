#!/usr/bin/env python3

from logging import shutdown
import rospy
from geometry_msgs.msg import PoseStamped
import numpy as np
from std_msgs.msg import Header
import message_filters



pose_vo = PoseStamped() 
pose_imu = PoseStamped()

def cb_vo(data):
    global pose_vo

    # pose_vo.header.seq = 1
    # pose_vo.header.stamp = data.header #header
    # pose_vo.header.frame_id = 'world'

    pose_vo.header = data.header
    pose_vo.pose.position = data.pose.position
    pose_vo.pose.orientation = data.pose.orientation


def cb_imu(data):
    global pose_imu

    # pose_imu.header.seq = 1
    # pose_imu.header.stamp = rospy.Time.now() #header
    # pose_imu.header.frame_id = 'world'

    pose_imu.header = data.header
    pose_imu.pose.position = data.pose.position
    pose_imu.pose.orientation = data.pose.orientation






# def vo_data(data):


def master_sync():

    def callback(vo_topic,imu_topic):

        # vo_sub = rospy.Subscriber('/vo_topic', PoseStamped,cb_vo)
        # imu_sub = rospy.Subscriber('/imu_topic', PoseStamped, cb_imu)
        # print(vo_topic)
        vo_pub.publish(vo_topic)
        imu_pub.publish(imu_topic)

    vo_pub = rospy.Publisher('sync_vo_topic',PoseStamped,queue_size=1)

    imu_pub  = rospy.Publisher('sync_imu_topic',PoseStamped,queue_size=1)

    rospy.init_node('master_sync',anonymous=True)

    rospy.loginfo("Initializing master sensor synchronization")

    rate = rospy.Rate(1)

    vo_sub = message_filters.Subscriber('/vo_topic', PoseStamped)

    imu_sub = message_filters.Subscriber('/imu_topic', PoseStamped)

    ts = message_filters.ApproximateTimeSynchronizer([vo_sub, imu_sub], 10,1)
    ts.registerCallback(callback)


    # vo_sub = rospy.Subscriber('/vo_topic', PoseStamped)
    # imu_sub = rospy.Subscriber('/imu_topic', PoseStamped)


        
    while not rospy.is_shutdown():
        
        # vo_pub.publish(pose_vo)
        # imu_pub.publish(pose_imu)

        rospy.spin()


if __name__ == '__main__':
    try:
       master_sync()
    except rospy.ROSInterruptException:
            pass



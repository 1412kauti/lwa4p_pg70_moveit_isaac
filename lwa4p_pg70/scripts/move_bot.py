import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import copy
from geometry_msgs.msg import Pose
from std_msgs.msg import String , Float32MultiArray

def callback(msg,move_group):
    x_position = msg.data[0]
    y_position = msg.data[1]
    # print (str(x_position) , str(y_position))

    horizontal_scale = 0.00105894065
    vertical_scale = 0.00111786963
    waypoints = []
    wpose = move_group.get_current_pose().pose
    
    if x_position > 640:
        wpose.position.y += horizontal_scale * x_position  # and sideways (y)
    else:
        wpose.position.y -= horizontal_scale * x_position  # and sideways (y)
    
    waypoints.append(copy.deepcopy(wpose))
        
    if y_position > 360:
        wpose.position.z += horizontal_scale * y_position  # and upwards (z)
    else:
        wpose.position.z -= horizontal_scale * y_position  # and upwards (z)

    waypoints.append(copy.deepcopy(wpose))
    
    (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0)  
    move_group.execute(plan,wait=True)

5
def move_robot():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("moveit_node", anonymous=True)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    display_trajectory_publisher = rospy.Publisher("/move_group/display_planned_path",moveit_msgs.msg.DisplayTrajectory,queue_size=10)
    pose_goal = Pose()
    pose_goal.position.x = -0.112967695994757
    pose_goal.position.y = 0.006018764998501226
    pose_goal.position.z = 0.5771371180896465
    pose_goal.orientation.x = 0.8105808128863473
    pose_goal.orientation.y = -0.00251992780272592
    pose_goal.orientation.z = 0.5856190782860292
    pose_goal.orientation.w = 0.0016403937941015566
    move_group.set_pose_target(pose_goal)
    move_group.go()
    rospy.Subscriber('co_ords',Float32MultiArray,callback,move_group)
    rospy.spin()
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    move_robot()
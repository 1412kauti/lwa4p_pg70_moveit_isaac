import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "arm"
move_group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher("/move_group/display_planned_path",moveit_msgs.msg.DisplayTrajectory,queue_size=10)

pose_goal = geometry_msgs.msg.Pose()
pose_goal.position.x = -0.112967695994757
pose_goal.position.y = 0.006018764998501226
pose_goal.position.z = 0.5771371180896465
pose_goal.orientation.x = 0.8105808128863473
pose_goal.orientation.y = -0.00251992780272592
pose_goal.orientation.z = 0.5856190782860292
pose_goal.orientation.w = 0.0016403937941015566
move_group.set_pose_target(pose_goal)
move_group.go(wait=True)
# Note: We are just planning, not asking move_group to actually move the robot yet:

current_pose = move_group.get_current_pose().pose
print(current_pose)
rospy.sleep(1)
moveit_commander.roscpp_shutdown()

0.7286781668663025, 0.8732059597969055, 2.3995991682568274e-07
import rospy
import subprocess
from std_msgs.msg import String

def callback_vision_onoff_cmd(data):
    node_name = data.data
    print('callback_vision_onoff_cmd starts..!')
    # turn off
    if is_node_running(node_name) == True:
        kill_cmd = 'rosnode kill ' + node_name
        subprocess.call(kill_cmd.split())
    # turn on
    subprocess.Popen('rosrun plaif_vision_server plaif_vision_node.py --config_path /home/plaif2/catkin_ws/config/bracket/config.yaml --node_id 0'.split())
    print('callback_vision_onoff_cmd terminates..!')

def callback_is_node_running(data):
    node_name = data.data
    is_running = is_node_running(node_name)
    print(node_name + ' is running : ' + str(is_running))
    pub = rospy.Publisher('is_node_running_result', String, queue_size=10)
    pub.publish(str(is_running))
    print('callback_is_node_running terminates..!')

# check if node_name is running
def is_node_running(node_name):
    print('rosnode list :')
    output = subprocess.check_output('rosnode list'.split())
    print(output)
    return True if node_name in output else False

def listener():
    rospy.init_node('plaif_node_onoff_mgr')

    # topic : node_onoff_cmd
    # msg type : std_msgs/String
    # data : {target_node_name}
    rospy.Subscriber('node_onoff_cmd', String, callback_vision_onoff_cmd)
    rospy.Subscriber('is_node_running', String, callback_is_node_running)
    rospy.spin()

if __name__ == '__main__':
    print('start plaif_node_onoff_mgr..!')
    listener()
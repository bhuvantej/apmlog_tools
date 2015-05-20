try:
	import rospy
	import rosbag
	from apmlog_tools.msg import AHR
except ImportError:
	print "Can't load ROS dependencies"

class AHRHandler:
	'''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		channel = logdata.channels[self.name]
		timestamp_ms = channel["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			msg = AHR()
			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.Alt = channel["Alt"].listData[msgid][1]
			msg.Lat = channel["Lat"].listData[msgid][1]
			msg.Lng = channel["Lng"].listData[msgid][1]
			msg.Roll = channel["Pitch"].listData[msgid][1]
			msg.Pitch = channel["Roll"].listData[msgid][1]
			msg.Yaw = channel["Yaw"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


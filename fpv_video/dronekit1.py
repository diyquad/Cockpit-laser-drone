from dronekit import connect, VehicleMode

connection_string='/dev/ttyACM0'
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string))
vehicle = connect(connection_string, wait_ready=False, baud=115200)
#vehicle = connect('udp:127.0.0.1:14550', wait_ready=True,baud=115200)

try:
    # Get some vehicle attributes (state)
    print "Get some vehicle attribute values:"
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s" % vehicle.mode.name    # settable

except KeyboardInterrupt:
    print "Cancelled"
    vehicle.close()


# Close vehicle object before exiting script
vehicle.close()

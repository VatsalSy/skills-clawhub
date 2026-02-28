# Ideas for ros2-skill Improvement

Based on analysis of [RosClaw](https://github.com/PlaiPin/rosclaw) and current ros2-skill implementation.

---

## Quick Wins (Few Lines of Code)

These can be implemented with minimal code changes:

### 1. Built-in Message Type Aliases — EASY ⭐
**Difficulty:** Easy | **Lines:** ~20

Add alias mapping for common message types:
```python
MSG_ALIASES = {
    "twist": "geometry_msgs/Twist",
    "twiststamped": "geometry_msgs/TwistStamped",
    "pose": "turtlesim/Pose",
    "odom": "nav_msgs/Odometry",
    "laserscan": "sensor_msgs/LaserScan",
    "image": "sensor_msgs/Image",
    "battery": "sensor_msgs/BatteryState",
}
# In get_msg_type(), check aliases first
```

---

### 2. Better Error Messages — ✅ IMPLEMENTED ⭐
**Difficulty:** Easy | **Lines:** ~30

**Status:** ✅ Implemented in ros2_skill v1.0.1

When message type not found, suggest solutions:
```python
if not msg_class:
    return output({
        "error": f"Unknown message type: {msg_type}",
        "hint": "Install package: sudo apt install ros-{DISTRO}-<package>",
        "alternatives": suggest_similar_types(msg_type)
    })
```

---

## Medium Effort (1-2 Hours)

### 3. Battery Monitoring
**Difficulty:** Medium | **Lines:** ~40

```python
def cmd_battery(args):
    """Read battery state from /battery_state"""
    rclpy.init()
    node = ROS2CLI("battery_monitor")
    battery_msg = None
    
    def callback(msg):
        nonlocal battery_msg
        battery_msg = msg
    
    sub = node.create_subscription(
        BatteryState, "/battery_state", callback, 10
    )
    
    # Spin briefly to get message
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)
    for _ in range(50):  # 5 seconds max
        executor.wait_once(timeout_sec=0.1)
        if battery_msg:
            break
    
    rclpy.shutdown()
    if battery_msg:
        output({
            "percentage": battery_msg.percentage * 100,
            "voltage": battery_msg.voltage,
            "current": battery_msg.current,
            "charging": battery_msg.charging
        })
    else:
        output({"error": "No battery data received"})
```

---

### 4. Timeout/Retry Configuration
**Difficulty:** Medium | **Lines:** ~30

Add global timeout argument:
```python
# In build_parser():
parser.add_argument("--timeout", type=float, default=5.0, help="Timeout in seconds")

# Use in all service/action calls
future = client.call_async(request)
end_time = time.time() + args.timeout
while time.time() < end_time and not future.done():
    rclpy.spin_once(node, timeout_sec=0.1)
```

---

## Higher Effort (Half Day+)

### 5. Camera/Snapshot Support
**Difficulty:** Hard | **Lines:** ~100+

Requires:
- Subscribe to `/camera/image_raw`
- Convert sensor_msgs/Image to base64 or save to file
- Handle different image encodings

---

### 6. Navigation (Nav2) Support
**Difficulty:** Hard | **Lines:** ~150+

Requires:
- Understand Nav2 action interface (`NavigateToPose`)
- Handle geometry_msgs/PoseStamped goals
- Track goal status and feedback

---

### 7. Robot Capabilities Auto-Discovery
**Difficulty:** Hard | **Lines:** ~200+

Requires:
- Scan all topics to detect sensors
- Check for action servers (Nav2, MoveIt)
- Build and cache robot profile
- Expose via `ros2_cli.py robot profile`

---

## Priority Summary

| Rank | Feature | Difficulty | Effort | Status |
|------|---------|------------|--------|--------|
| 1 | Message Type Aliases | ⭐ Easy | 20 min | Pending |
| 2 | Better Error Messages | ⭐ Easy | 10 min | ✅ Done |
| 3 | Battery Monitoring | Medium | 1 hr | Pending |
| 4 | Timeout Config | Medium | 1 hr | Pending |
| 5 | Camera Snapshot | Hard | 2-3 hr | Pending |
| 6 | Nav2 Support | Hard | 3-4 hr | Pending |
| 7 | Auto-Discovery | Hard | 4-5 hr | Pending |

---

## Comparison with RosClaw

| Feature | ros2-skill | RosClaw |
|---------|------------|---------|
| Communication | rclpy (direct) | rosbridge (WebSocket) |
| Language | Python | TypeScript + Python |
| Estop | ✅ | ✅ |
| Camera snapshot | ❌ | ✅ |
| Battery monitor | ❌ | ✅ |
| Nav2 support | ❌ | ✅ |
| Auto-discovery | ❌ | ✅ |
| Robot profiles | ❌ | ✅ |

---

## Recommended Next Steps

1. **Add message aliases** — 20 lines, allows users to use short names (e.g., "twist" instead of "geometry_msgs/Twist")
2. **Battery monitor** — 1 hour, common use case for mobile robots
3. **Timeout configuration** — 1 hour, improves reliability
4. **Camera snapshot** — 2-3 hours, enables vision-based workflows

The error messages are now helpful - next focus is on making it easier to specify message types.

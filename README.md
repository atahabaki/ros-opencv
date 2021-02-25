# ROS + OpenCV for a specific mission

Uses OpenCV for detecting object, ROS for controlling the device. And ArduPilot for autonomous...

## Meet with Nodes

Let me tell you, what every single node I've written is doing...

### Philosopher

It was designed to control, and maintain everything (arming, servo controlling, mood changing, and etc.)...
That way, I could simply do whatever I want. For testing purposes, I've written that in a infinite `Tsukiyomi` loop :ok_hand:

### Passanger

Keeps track of Waypoints, which one is reached...
It's a server too, but I couldn't even tested ('cause of the hardware...)

```
uint16 wp_seq
```

### GPSTracker

As the name tells its job, it tells where the drone is.

```
float64 latitude
float64 longitude
float64 altitude
```

### Finder

Tries to find the predefined object by ImageProcessing via OpenCV.
It's a basic server, which always returns (by design of :poop: it should be...)

```
uint64 cx
uint64 cy
float32 distance
float32 distance_percentage
float32 angle
```

It could open up a window of what camera sees, that was for completely test cases.

### TankManager

Controls the servo... It's a basic subscriber, I mean it's listening for an order to turn the servo...
  

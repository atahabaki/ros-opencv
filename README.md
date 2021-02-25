# ROS + OpenCV for a specific mission

Uses OpenCV for detecting a predefined object, ROS for controlling the device. And ArduPilot for autonomous...

## Meet with Nodes

Let me tell you, what every single node I've written is doing...

### Philosopher

It was designed to control, and maintain everything (arming, servo controlling, mood changing, and etc.)...
That way, I could simply do whatever I want. For testing purposes, I've written that in an infinite `Tsukiyomi` loop :ok_hand:

### Passanger

I know I named it wrong but it's too late to change, I no longer actively developing this :poop:. So it's :100:% fine for me.
Keeps track of Waypoints, which one is reached...
It's a server too, but I couldn't even test that ('cause of the hardware...)

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
It's a basic server, which always returns (by the design of :poop: it should be...)

```
uint64 cx
uint64 cy
float32 distance
float32 distance_percentage
float32 angle
```

It could open up a window of what the camera sees, that was for completely test cases.

### TankManager

Controls the servo... It's a basic subscriber, I mean it's listening for an order to turn the servo...
  

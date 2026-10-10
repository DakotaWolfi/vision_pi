# Architecture

```text
                    VisionPi
                       │
       ┌───────────────┼────────────────┐
       │               │                │
    Cameras          HUD/Menu         System
       │               │                │
 CSI + WiFi Eyes   Hand gestures   Temp/Fan/FPS
       │               │                │
       └───────────────┼────────────────┘
                       │
                 Collar client
                       │
                 CollarPet runtime
```

Principle: VisionPi is a UI/vision system. CollarPet remains authoritative for
CollarPet behaviour, sensors and outputs.

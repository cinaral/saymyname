%% 0 - Carry the aquarium
% Cost Removability Durability Aesthetics Manufacturability
input_carry = [1 1/5 1/7 1/3 5; 0 1 3 7 5; 0 0 1 7 1; 0 0 0 1 1/5; 0 0 0 0 1]
weight_carry = calculateahpweight(input_carry)
% Glue Gravity Holes Directly Segmented
pugh_carry = [1 1 0 0 -1; -1 1 0 -1 -1; 1 1 0 -1 -1; -1 1 0 -1 1; 1 -1 0 -1 -1]
sum(pugh_carry .* weight_carry, 1)

%% 1. Detect the fish
% Resolution ResponseTime Cost Mountability Upgradability
input_detectFish = [1 1 7 3 3; 0 1 5 3 5; 0 0 1 1/3 1/3; 0 0 0 1 3; 0 0 0 0 1]
weight_detectFish = calculateahpweight(input_detectFish)
% WebcamRaspberry Esp32cam RaspberryCam
pugh_detectFish = [0 -1 -1; 0 -1 1; 0 1 1; 0 -1 -1; 0 -1 0]
sum(pugh_detectFish .* weight_detectFish, 1)

%% 2. Detect obstacles
% Precision Cost ResponseTime Manufacturability
input_detectObstacles = [1 5 1 3; 0 1 1/5 1/3; 0 0 1 5; 0 0 0 1]
weight_detectObstacles = calculateahpweight(input_detectObstacles)
% Ultrasonic CameraOnRobot OverheadCamera
pugh_detectObstacles = [0 -1 -1; 0 -1 -1; 0 -1 -1; 0 0 -1]
sum(pugh_detectObstacles .* weight_detectObstacles, 1)

%% 3. Facilitate the movement
% Smoothness RangeOfMotion Cost Durability Manufacturability
input_facilMovement = [1 3 7 5 3; 0 1 5 3 3; 0 0 1 1/3 1/3; 0 0 0 1 3; 0 0 0 0 1]
weight_facilMovement = calculateahpweight(input_facilMovement)
% PrintedMecha MachinedMecha Differential Tracks Steering
pugh_facilMovement = [1 1 0 0 0; 1 1 0 0 -1; 0 -1 0 -1 -1; -1 0 0 1 -1; 1 -1 0 -1 -1]
sum(pugh_facilMovement .* weight_facilMovement, 1)

%% 4. Actuate the movement
% Noise Precision Durability Cost EaseOfControl
input_actuate = [1 1/5 1/3 3 1/5; 0 1 1 5 3; 0 0 1 5 3; 0 0 0 1 3; 0 0 0 0 1];
weight_actuate = calculateahpweight(input_actuate)
% Brushless Brushed Stepper
pugh_actuate = [1 0 0; 0 0 1; 1 0 -1; -1 0 -1; -1 0 1]
sum(pugh_actuate .* weight_actuate, 1)

%% 5. Control the movement
% Cost Performance Upgradability Continuity
input_control = [1 1/5 1/3 1/5; 0 1 3 3; 0 0 1 1/3; 0 0 0 1]
weight_control = calculateahpweight(input_control)
% Raspberry NetworkModule+PC Arduino
pugh_control = [-1 -1 0; 1 1 0; 1 1 0; 0 -1 0]
sum(pugh_control .* weight_control, 1)

%% 5.5 Detect the current position of the robot
% Cost ResponseTime Precision Manufacturability
input_detectPosition = [1 1/5 1/5 1/3; 0 1 1 3; 0 0 1 3; 0 0 0 1]
weight_detectPosition = calculateahpweight(input_detectPosition)
% OverheadCamera CameraOnTheRobot Cameraless
pugh_detectPosition = [0 -1 1; 0 1 1; 0 1 -1; 0 1 1]
sum(pugh_detectPosition .* weight_detectPosition, 1)

%% 6. Send and receive messages over the network
% Cost Performance Upgradability
input_network = [1 1/5 1/5; 0 1 3; 0 0 1]
weight_network = calculateahpweight(input_network)
% Raspberry NetworkModule ArduinoNetworkModule
pugh_network = [-1 0 -1; 1 0 0; 1 0 0]
sum(pugh_network .* weight_network, 1)

%% 7. Display the current status to nearby observers 
% Cost Manufacturability Aesthetics RangeOfMessages PowerConsumption
input_display = [1 1/3 1/3 1/3 1/5; 0 1 1/5 1/3 1/3; 0 0 1 1/3 1/3; 0 0 0 1 1/3; 0 0 0 0 1]
weight_display =  calculateahpweight(input_display)
% Led Speaker Monitor
pugh_display = [0 -1 -1; 0 -1 -1; 0 0 1; 0 1 1; 0 -1 -1]
sum(pugh_display .* weight_display, 1)

%% 8. Communicate with the fish
% Cost Manufacturability RangeOfMessages PowerConsumption 
input_communicate = [1 1/3 1/3 1/5; 0 1 1/3 1/3; 0 0 1 1/3; 0 0 0 1]
weight_communicate = calculateahpweight(input_communicate)
% Led Monitor
pugh_communicate = [0 -1; 0 -1; 0 1; 0 -1]
sum(pugh_communicate .* weight_communicate, 1)

%% 9. Contain the water and fish
% Cost Mountability Weight Visibility Aesthetics
input_aquarium = [1 1/5 1/3 1/3 1/3; 0 1 3 3 3; 0 0 1 3 3; 0 0 0 1 3; 0 0 0 0 1]
weight_aquarium = calculateahpweight(input_aquarium)
% Plastic GlassSpherical GlassPrismatic
pugh_aquarium = [1 0 -1; 1 0 1; 1 0 0; 1 0 1; -1 0 -1]
sum(pugh_aquarium .* weight_aquarium, 1)

%% 10. Store the power
% Cost Durability CapacityPerWeight
input_battery = [1 1/3 1/3; 0 1 3; 0 0 1]
weight_battery = calculateahpweight(input_battery)
% NiCad LiPo LiIon Dry
pugh_battery = [1 -1 0 1; -1 1 0 1; -1 -1 0 -1]
sum(pugh_battery .* weight_battery, 1)

%% 11. Charge the storage
% Cost Manufacturability ChargingTime Durability
input_charging = [1 1/5 1/3 1/3; 0 1 5 3; 0 0 1 1/3; 0 0 0 1]
weight_charging = calculateahpweight(input_charging)
% DanglingRoomMagnet DanglingRobotMagnet Mechanical Inductive
pugh_charging = [1 1 0 -1; 1 1 0 -1; 0 0 0 -1; 1 1 0 1]
sum(pugh_charging .* weight_charging, 1)

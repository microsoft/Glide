#include <micro_ros_arduino.h>

#include <arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rmw_microros/rmw_microros.h>

#include <std_msgs/msg/int32.h>
#include <geometry_msgs/msg/twist.h>

#include "HX711.h" // Rob Tillaart library

#define LED_PIN 13
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){return false;}}
#define EXECUTE_EVERY_N_MS(MS, X)  do { \
  static volatile int64_t init = -1; \
  if (init == -1) { init = uxr_millis();} \
  if (uxr_millis() - init > MS) { X; init = uxr_millis();} \
} while (0)\

rclc_support_t support;
rcl_node_t node;
rcl_timer_t timer;
rclc_executor_t executor;
rcl_allocator_t allocator;
rcl_publisher_t publisher_timer;
rcl_publisher_t publisher_torque;
rcl_publisher_t publisher_odometry_left;
rcl_publisher_t publisher_odometry_right;
rcl_subscription_t subscriber_haptic;
rcl_subscription_t subscriber_cmdvel;
std_msgs__msg__Int32 msg_timer;
std_msgs__msg__Int32 msg_torque;
std_msgs__msg__Int32 msg_odometry_left;
std_msgs__msg__Int32 msg_odometry_right;
std_msgs__msg__Int32 msg_haptic;
geometry_msgs__msg__Twist cmd_vel;
bool micro_ros_init_successful;

#pragma region wheel encoder variables
//Wheel encoder quadrature outputs
const int CHA_R = 38;
const int CHB_R = 39;
const int CHA_L = 40;
const int CHB_L = 41;

volatile int master_count_L = 0; // universal wheel rev count for left wheel
volatile int master_count_R = 0; // universal rev count for right wheel
volatile byte INTFLAG_L = 0; // interrupt status flag for left encoder
volatile byte INTFLAG_R = 0; // interrupt status flag for right encoder
volatile int Lincr, Rincr;  // left and right wheel enc increments
#pragma endregion

#pragma region HX711 Torque globals
HX711 TorqueSensor;

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 17;
const int LOADCELL_SCK_PIN = 16;

int Torque = 0; //Torque from torque sensor on handle.  Via I2C comm
float TorqueFlt = 0; //handle torque avg filtered value to reduce drift
#pragma endregion

#pragma region Haptic Actuator globals
const int GESTURE_DIRATION = 50;
const int ACTUATOR_COUNT = 6;
int Actuator[6] = {9, 10, 11, 12, 24, 25}; //Glide handle actuators

enum hapticGestures {#include <micro_ros_arduino.h>

#include <arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rmw_microros/rmw_microros.h>

#include <std_msgs/msg/int32.h>
#include <geometry_msgs/msg/twist.h>

#include "HX711.h" // Rob Tillaart library

#define LED_PIN 13
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){return false;}}
#define EXECUTE_EVERY_N_MS(MS, X)  do { \
  static volatile int64_t init = -1; \
  if (init == -1) { init = uxr_millis();} \
  if (uxr_millis() - init > MS) { X; init = uxr_millis();} \
} while (0)\

rclc_support_t support;
rcl_node_t node;
rcl_timer_t timer;
rclc_executor_t executor;
rcl_allocator_t allocator;
rcl_publisher_t publisher_timer;
rcl_publisher_t publisher_torque;
rcl_publisher_t publisher_odometry_left;
rcl_publisher_t publisher_odometry_right;
rcl_subscription_t subscriber_haptic;
rcl_subscription_t subscriber_cmdvel;
std_msgs__msg__Int32 msg_timer;
std_msgs__msg__Int32 msg_torque;
std_msgs__msg__Int32 msg_odometry_left;
std_msgs__msg__Int32 msg_odometry_right;
std_msgs__msg__Int32 msg_haptic;
geometry_msgs__msg__Twist cmd_vel;
bool micro_ros_init_successful;

#pragma region wheel encoder variables
//Wheel encoder quadrature outputs
const int CHA_R = 38;
const int CHB_R = 39;
const int CHA_L = 40;
const int CHB_L = 41;

volatile int master_count_L = 0; // universal wheel rev count for left wheel
volatile int master_count_R = 0; // universal rev count for right wheel
volatile byte INTFLAG_L = 0; // interrupt status flag for left encoder
volatile byte INTFLAG_R = 0; // interrupt status flag for right encoder
volatile int Lincr, Rincr;  // left and right wheel enc increments
#pragma endregion

#pragma region HX711 Torque globals
HX711 TorqueSensor;

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 17;
const int LOADCELL_SCK_PIN = 16;

int Torque = 0; //Torque from torque sensor on handle.  Via I2C comm
float TorqueFlt = 0; //handle torque avg filtered value to reduce drift
#pragma endregion

#pragma region Haptic Actuator globals
const int GESTURE_DIRATION = 50;
const int ACTUATOR_COUNT = 6;
int Actuator[6] = {9, 10, 11, 12, 24, 25}; //Glide handle actuators

enum hapticGestures {
  ALL_OFF,
  ALL_ON,
  LEFT_TURN,
  RIGHT_TURN
} hapticGesture;

hapticGestures currentGesture = ALL_OFF;
unsigned long currentGestureEnd = 0;
#pragma endregion

#define DEBUG_DIAGNOSTIC_PIN 0

enum states {
  WAITING_AGENT,
  AGENT_AVAILABLE,
  AGENT_CONNECTED,
  AGENT_DISCONNECTED
} state;

void set_haptic_gesture(hapticGestures new_gesture)
{
  currentGesture = new_gesture;
  currentGestureEnd = rmw_uros_epoch_millis() + GESTURE_DIRATION;

  int actuator_idx;
  switch(currentGesture)
  {
    case ALL_OFF:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], LOW); //turn off
        }
        break;
    case ALL_ON:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], LOW); //turn off
        }
        break;
    case LEFT_TURN:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT/2 ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], HIGH);
        }
        break;
    case RIGHT_TURN:
        for (actuator_idx = ACTUATOR_COUNT/2; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], HIGH);
        }
        break;
    default:
        break;
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
  (void) last_call_time;
  if (timer != NULL) {
    rcl_publish(&publisher_timer, &msg_timer, NULL);
    msg_timer.data++;

    msg_odometry_left.data = master_count_L;
    msg_odometry_right.data = master_count_R;

    // immediately reset counters
    master_count_L = 0;
    master_count_R = 0;

    rcl_publish(&publisher_odometry_left, &msg_odometry_left, NULL);
    rcl_publish(&publisher_odometry_right, &msg_odometry_right, NULL);
  }
}

void cmd_vel_callback(const void * msgin)
{
  geometry_msgs__msg__Twist * msg = (geometry_msgs__msg__Twist *) msgin;
  // TODO actuate haptic break gesture  
}

void haptic_callback(const void * msgin)
{
  std_msgs__msg__Int32 * msg = (std_msgs__msg__Int32 *) msgin;
  hapticGestures new_gesture = (hapticGestures)msg->data;
  set_haptic_gesture(new_gesture);
}

// Functions create_entities and destroy_entities can take several seconds.
// In order to reduce this rebuild the library with
// - RMW_UXRCE_ENTITY_CREATION_DESTROY_TIMEOUT=0
// - UCLIENT_MAX_SESSION_CONNECTION_ATTEMPTS=3

bool create_entities()
{
  allocator = rcl_get_default_allocator();

  // create init_options
  int argc = 0;
  char ** argv = NULL;
  RCCHECK(rclc_support_init(&support, argc, argv, &allocator));

  // create node
  const char * node_name = "microROS_node";
  const char * node_namespace = ""; // Node namespace (Can remain empty "")
  RCCHECK(rclc_node_init_default(&node, node_name, node_namespace, &support));

  // create publisher_timer
  RCCHECK(rclc_publisher_init_default(
    &publisher_timer,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/heartbeat"));

  // create publisher_torque
  RCCHECK(rclc_publisher_init_default(
    &publisher_torque,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/torque"));

  // create publisher_odometry_left
  RCCHECK(rclc_publisher_init_default(
    &publisher_odometry_left,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/odometry_left"));

  // create publisher_odometry_right
  RCCHECK(rclc_publisher_init_default(
    &publisher_odometry_right,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/odometry_right"));

  // create subscription
  RCCHECK(rclc_subscription_init_default(
    &subscriber_haptic,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/haptic"
  ));

  RCCHECK(rclc_subscription_init_best_effort(
    &subscriber_cmdvel,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
    "cmd_vel"));

  // create executor
  // NOTE: If adding a timer or subscription, you MUST update num_timers and/or num_subscriptions!
  const int num_timers = 1;
  const int num_subscriptions = 2;
  const int num_handles = num_timers + num_subscriptions;

  executor = rclc_executor_get_zero_initialized_executor();
  RCCHECK(rclc_executor_init(
    &executor,
    &support.context,
    num_handles, 
    &allocator));
  
  RCCHECK(rclc_executor_add_timer(
    &executor,
    &timer));
  RCCHECK(rclc_executor_add_subscription(
    &executor, 
    &subscriber_haptic, 
    &msg_haptic, 
    haptic_callback, 
    ON_NEW_DATA));
  RCCHECK(rclc_executor_add_subscription(
    &executor, 
    &subscriber_cmdvel, 
    &cmd_vel, 
    cmd_vel_callback, 
    ON_NEW_DATA));
  
  // create timer,
  const unsigned int timer_timeout = 1000;
  RCCHECK(rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(timer_timeout),
    timer_callback));

  return true;
}

void destroy_entities()
{
  rmw_context_t * rmw_context = rcl_context_get_rmw_context(&support.context);
  (void) rmw_uros_set_context_entity_destroy_session_timeout(rmw_context, 0);

  rcl_publisher_fini(&publisher_timer, &node);
  rcl_publisher_fini(&publisher_torque, &node);
  rcl_publisher_fini(&publisher_odometry_left, &node);
  rcl_publisher_fini(&publisher_odometry_right, &node);
  rcl_subscription_fini(&subscriber_haptic, &node);
  rcl_subscription_fini(&subscriber_cmdvel, &node);

  rcl_timer_fini(&timer);
  rclc_executor_fini(&executor);
  rcl_node_fini(&node);
  rclc_support_fini(&support);
}

void initialize_wheel_encoders()
{
    //Wheel enc pins init
  pinMode(CHA_L, INPUT_PULLUP); //left wheel encoder A with an internal pulluip resistor
  pinMode(CHB_L, INPUT_PULLUP);
  pinMode(CHA_R, INPUT_PULLUP); //right  wheel encoder A
  pinMode(CHB_R, INPUT_PULLUP);

  //wheel enc ISR
  attachInterrupt(CHA_L, Flag_L, RISING); //format OK for Teensy4.1
  attachInterrupt(CHA_R, Flag_R, RISING);
}

void initialize_haptic_actuators()
{
  // initialize the Haptic output digital pins as an outputs for haptic actuators.
  for (int actuator_idx = 0; actuator_idx < ACTUATOR_COUNT; actuator_idx++) //make all actuator pins output
  {
    pinMode(Actuator[actuator_idx], OUTPUT);
    digitalWrite(Actuator[actuator_idx], LOW);
  }
}

void initialize_torque_sensor()
{
  TorqueSensor.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN); //torque sensor (I2C comm)
}

void Flag_L() {
  INTFLAG_L = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_L) && !digitalRead(CHB_L)) {
    master_count_L-- ;
    Lincr = -1;
  }
  else
  {
    // subtract 1 from count for CCW
    //if (digitalRead(CHA_L) && digitalRead(CHB_L)) {
    master_count_L++ ;
    Lincr = 1;
  }
}

void Flag_R() {
  INTFLAG_R = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_R) && !digitalRead(CHB_R)) {
    master_count_R++ ;
    Rincr = 1;
  }

  // else subtract 1 from count for CCW
  if (digitalRead(CHA_R) && digitalRead(CHB_R)) {
    master_count_R--;
    Rincr = -1;
  }
}

void setup() {
  set_microros_transports();

  initialize_wheel_encoders();

  initialize_haptic_actuators();

  initialize_torque_sensor();
  
  pinMode(LED_PIN, OUTPUT);

  state = WAITING_AGENT;

  msg_timer.data = 0;
  msg_torque.data = 0;
  msg_odometry_left.data = 0;
  msg_odometry_right.data = 0;
}

void loop() {
  switch (state) {
    case WAITING_AGENT:
      EXECUTE_EVERY_N_MS(500, state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_AVAILABLE : WAITING_AGENT;);
      break;
    case AGENT_AVAILABLE:
      state = (true == create_entities()) ? AGENT_CONNECTED : WAITING_AGENT;
      if (state == WAITING_AGENT) {
        destroy_entities();
      };
      break;
    case AGENT_CONNECTED:
      EXECUTE_EVERY_N_MS(200, state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_CONNECTED : AGENT_DISCONNECTED;);
      if (state == AGENT_CONNECTED) {
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
      }
      break;
    case AGENT_DISCONNECTED:
      destroy_entities();
      state = WAITING_AGENT;
      break;
    default:
      break;
  }

  if (state == AGENT_CONNECTED) {
    digitalWrite(LED_PIN, HIGH);

    digitalWrite(DEBUG_DIAGNOSTIC_PIN, HIGH); //diagnostic pin. Pulse every lo
  
    if (TorqueSensor.is_ready()) {  //read strain guage torque sensor thru I2C comm
      long Torque = TorqueSensor.read(); //I2C read torque sensor
      Torque = Torque + 118000.0; //offset
      Torque = Torque >> 8; //scale down

      msg_torque.data = (int32_t)Torque;
      rcl_publish(&publisher_torque, &msg_torque, NULL);
    }
  
    digitalWrite(DEBUG_DIAGNOSTIC_PIN, LOW); //diagnostic time
  
    if (INTFLAG_L)   {    //Check to see if interrupt from left encoder
      INTFLAG_L = 0;  //clr interrupt flag
    }
  
    if (INTFLAG_R)   {    //if interrupt from right encoder
      INTFLAG_R = 0; // clear flag
    }
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  unsigned long timeNow = rmw_uros_epoch_millis();
  if (currentGestureEnd < timeNow)
  {
    set_haptic_gesture(ALL_OFF);
  }
}
  ALL_OFF,
  ALL_ON,
  LEFT_TURN,
  RIGHT_TURN
} hapticGesture;

hapticGestures currentGesture = ALL_OFF;
unsigned long currentGestureEnd = 0;
#pragma endregion

#define DEBUG_DIAGNOSTIC_PIN 0

enum states {
  WAITING_AGENT,
  AGENT_AVAILABLE,
  AGENT_CONNECTED,
  AGENT_DISCONNECTED
} state;

void set_haptic_gesture(hapticGestures new_gesture)
{
  currentGesture = new_gesture;
  currentGestureEnd = rmw_uros_epoch_millis() + GESTURE_DIRATION;

  int actuator_idx;
  switch(currentGesture)
  {
    case ALL_OFF:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], LOW); //turn off
        }
        break;
    case ALL_ON:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], LOW); //turn off
        }
        break;
    case LEFT_TURN:
        for (actuator_idx = 0; actuator_idx < ACTUATOR_COUNT/2 ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], HIGH);
        }
        break;
    case RIGHT_TURN:
        for (actuator_idx = ACTUATOR_COUNT/2; actuator_idx < ACTUATOR_COUNT ; actuator_idx++)
        {
          digitalWrite(Actuator[actuator_idx], HIGH);
        }
        break;
    default:
        break;
  }
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
  (void) last_call_time;
  if (timer != NULL) {
    rcl_publish(&publisher_timer, &msg_timer, NULL);
    msg_timer.data++;

    msg_odometry_left.data = master_count_L;
    msg_odometry_right.data = master_count_R;

    // immediately reset counters
    master_count_L = 0;
    master_count_R = 0;

    rcl_publish(&publisher_odometry_left, &msg_odometry_left, NULL);
    rcl_publish(&publisher_odometry_right, &msg_odometry_right, NULL);
  }
}

void cmd_vel_callback(const void * msgin)
{
  geometry_msgs__msg__Twist * msg = (geometry_msgs__msg__Twist *) msgin;
  // TODO actuate haptic break gesture  
}

void haptic_callback(const void * msgin)
{
  std_msgs__msg__Int32 * msg = (std_msgs__msg__Int32 *) msgin;
  hapticGestures new_gesture = (hapticGestures)msg->data;
  set_haptic_gesture(new_gesture);
}

// Functions create_entities and destroy_entities can take several seconds.
// In order to reduce this rebuild the library with
// - RMW_UXRCE_ENTITY_CREATION_DESTROY_TIMEOUT=0
// - UCLIENT_MAX_SESSION_CONNECTION_ATTEMPTS=3

bool create_entities()
{
  allocator = rcl_get_default_allocator();

  // create init_options
  int argc = 0;
  char ** argv = NULL;
  RCCHECK(rclc_support_init(&support, argc, argv, &allocator));

  // create node
  const char * node_name = "microROS_node";
  const char * node_namespace = ""; // Node namespace (Can remain empty "")
  RCCHECK(rclc_node_init_default(&node, node_name, node_namespace, &support));

  // create publisher_timer
  RCCHECK(rclc_publisher_init_default(
    &publisher_timer,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/heartbeat"));

  // create publisher_torque
  RCCHECK(rclc_publisher_init_default(
    &publisher_torque,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/torque"));

  // create publisher_odometry_left
  RCCHECK(rclc_publisher_init_default(
    &publisher_odometry_left,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/odometry_left"));

  // create publisher_odometry_right
  RCCHECK(rclc_publisher_init_default(
    &publisher_odometry_right,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/odometry_right"));

  // create subscription
  RCCHECK(rclc_subscription_init_default(
    &subscriber_haptic,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "/microROS/haptic"
  ));

  RCCHECK(rclc_subscription_init_best_effort(
    &subscriber_cmdvel,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
    "cmd_vel"));

  // create executor
  // NOTE: If adding a timer or subscription, you MUST update num_timers and/or num_subscriptions!
  const int num_timers = 1;
  const int num_subscriptions = 2;
  const int num_handles = num_timers + num_subscriptions;

  executor = rclc_executor_get_zero_initialized_executor();
  RCCHECK(rclc_executor_init(
    &executor,
    &support.context,
    num_handles, 
    &allocator));
  
  RCCHECK(rclc_executor_add_timer(
    &executor,
    &timer));
  RCCHECK(rclc_executor_add_subscription(
    &executor, 
    &subscriber_haptic, 
    &msg_haptic, 
    haptic_callback, 
    ON_NEW_DATA));
  RCCHECK(rclc_executor_add_subscription(
    &executor, 
    &subscriber_cmdvel, 
    &cmd_vel, 
    cmd_vel_callback, 
    ON_NEW_DATA));
  
  // create timer,
  const unsigned int timer_timeout = 1000;
  RCCHECK(rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(timer_timeout),
    timer_callback));

  return true;
}

void destroy_entities()
{
  rmw_context_t * rmw_context = rcl_context_get_rmw_context(&support.context);
  (void) rmw_uros_set_context_entity_destroy_session_timeout(rmw_context, 0);

  rcl_publisher_fini(&publisher_timer, &node);
  rcl_publisher_fini(&publisher_torque, &node);
  rcl_publisher_fini(&publisher_odometry_left, &node);
  rcl_publisher_fini(&publisher_odometry_right, &node);
  rcl_subscription_fini(&subscriber_haptic, &node);
  rcl_subscription_fini(&subscriber_cmdvel, &node);

  rcl_timer_fini(&timer);
  rclc_executor_fini(&executor);
  rcl_node_fini(&node);
  rclc_support_fini(&support);
}

void initialize_wheel_encoders()
{
    //Wheel enc pins init
  pinMode(CHA_L, INPUT_PULLUP); //left wheel encoder A with an internal pulluip resistor
  pinMode(CHB_L, INPUT_PULLUP);
  pinMode(CHA_R, INPUT_PULLUP); //right  wheel encoder A
  pinMode(CHB_R, INPUT_PULLUP);

  //wheel enc ISR
  attachInterrupt(CHA_L, Flag_L, RISING); //format OK for Teensy4.1
  attachInterrupt(CHA_R, Flag_R, RISING);
}

void initialize_haptic_actuators()
{
  // initialize the Haptic output digital pins as an outputs for haptic actuators.
  for (int actuator_idx = 0; actuator_idx < ACTUATOR_COUNT; actuator_idx++) //make all actuator pins output
  {
    pinMode(Actuator[actuator_idx], OUTPUT);
    digitalWrite(Actuator[actuator_idx], LOW);
  }
}

void initialize_torque_sensor()
{
  TorqueSensor.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN); //torque sensor (I2C comm)
}

void Flag_L() {
  INTFLAG_L = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_L) && !digitalRead(CHB_L)) {
    master_count_L-- ;
    Lincr = -1;
  }
  else
  {
    // subtract 1 from count for CCW
    //if (digitalRead(CHA_L) && digitalRead(CHB_L)) {
    master_count_L++ ;
    Lincr = 1;
  }
}

void Flag_R() {
  INTFLAG_R = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_R) && !digitalRead(CHB_R)) {
    master_count_R++ ;
    Rincr = 1;
  }

  // else subtract 1 from count for CCW
  if (digitalRead(CHA_R) && digitalRead(CHB_R)) {
    master_count_R--;
    Rincr = -1;
  }
}

void setup() {
  set_microros_transports();

  initialize_wheel_encoders();

  initialize_haptic_actuators();

  initialize_torque_sensor();
  
  pinMode(LED_PIN, OUTPUT);

  state = WAITING_AGENT;

  msg_timer.data = 0;
  msg_torque.data = 0;
  msg_odometry_left.data = 0;
  msg_odometry_right.data = 0;
}

void loop() {
  switch (state) {
    case WAITING_AGENT:
      EXECUTE_EVERY_N_MS(500, state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_AVAILABLE : WAITING_AGENT;);
      break;
    case AGENT_AVAILABLE:
      state = (true == create_entities()) ? AGENT_CONNECTED : WAITING_AGENT;
      if (state == WAITING_AGENT) {
        destroy_entities();
      };
      break;
    case AGENT_CONNECTED:
      EXECUTE_EVERY_N_MS(200, state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_CONNECTED : AGENT_DISCONNECTED;);
      if (state == AGENT_CONNECTED) {
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
      }
      break;
    case AGENT_DISCONNECTED:
      destroy_entities();
      state = WAITING_AGENT;
      break;
    default:
      break;
  }

  if (state == AGENT_CONNECTED) {
    digitalWrite(LED_PIN, HIGH);

    digitalWrite(DEBUG_DIAGNOSTIC_PIN, HIGH); //diagnostic pin. Pulse every lo
  
    if (TorqueSensor.is_ready()) {  //read strain guage torque sensor thru I2C comm
      long Torque = TorqueSensor.read(); //I2C read torque sensor
      Torque = Torque + 118000.0; //offset
      Torque = Torque >> 8; //scale down

      msg_torque.data = (int32_t)Torque;
      rcl_publish(&publisher_torque, &msg_torque, NULL);
    }
  
    digitalWrite(DEBUG_DIAGNOSTIC_PIN, LOW); //diagnostic time
  
    if (INTFLAG_L)   {    //Check to see if interrupt from left encoder
      INTFLAG_L = 0;  //clr interrupt flag
    }
  
    if (INTFLAG_R)   {    //if interrupt from right encoder
      INTFLAG_R = 0; // clear flag
    }
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  unsigned long timeNow = rmw_uros_epoch_millis();
  if (currentGestureEnd < timeNow)
  {
    set_haptic_gesture(ALL_OFF);
  }
}
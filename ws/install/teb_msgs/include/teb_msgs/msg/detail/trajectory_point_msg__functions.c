// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from teb_msgs:msg/TrajectoryPointMsg.idl
// generated code does not contain a copyright notice
#include "teb_msgs/msg/detail/trajectory_point_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `velocity`
// Member `acceleration`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `time_from_start`
#include "builtin_interfaces/msg/detail/duration__functions.h"

bool
teb_msgs__msg__TrajectoryPointMsg__init(teb_msgs__msg__TrajectoryPointMsg * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    teb_msgs__msg__TrajectoryPointMsg__fini(msg);
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__init(&msg->velocity)) {
    teb_msgs__msg__TrajectoryPointMsg__fini(msg);
    return false;
  }
  // acceleration
  if (!geometry_msgs__msg__Twist__init(&msg->acceleration)) {
    teb_msgs__msg__TrajectoryPointMsg__fini(msg);
    return false;
  }
  // time_from_start
  if (!builtin_interfaces__msg__Duration__init(&msg->time_from_start)) {
    teb_msgs__msg__TrajectoryPointMsg__fini(msg);
    return false;
  }
  return true;
}

void
teb_msgs__msg__TrajectoryPointMsg__fini(teb_msgs__msg__TrajectoryPointMsg * msg)
{
  if (!msg) {
    return;
  }
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // velocity
  geometry_msgs__msg__Twist__fini(&msg->velocity);
  // acceleration
  geometry_msgs__msg__Twist__fini(&msg->acceleration);
  // time_from_start
  builtin_interfaces__msg__Duration__fini(&msg->time_from_start);
}

teb_msgs__msg__TrajectoryPointMsg *
teb_msgs__msg__TrajectoryPointMsg__create()
{
  teb_msgs__msg__TrajectoryPointMsg * msg = (teb_msgs__msg__TrajectoryPointMsg *)malloc(sizeof(teb_msgs__msg__TrajectoryPointMsg));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(teb_msgs__msg__TrajectoryPointMsg));
  bool success = teb_msgs__msg__TrajectoryPointMsg__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
teb_msgs__msg__TrajectoryPointMsg__destroy(teb_msgs__msg__TrajectoryPointMsg * msg)
{
  if (msg) {
    teb_msgs__msg__TrajectoryPointMsg__fini(msg);
  }
  free(msg);
}


bool
teb_msgs__msg__TrajectoryPointMsg__Sequence__init(teb_msgs__msg__TrajectoryPointMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  teb_msgs__msg__TrajectoryPointMsg * data = NULL;
  if (size) {
    data = (teb_msgs__msg__TrajectoryPointMsg *)calloc(size, sizeof(teb_msgs__msg__TrajectoryPointMsg));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = teb_msgs__msg__TrajectoryPointMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        teb_msgs__msg__TrajectoryPointMsg__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
teb_msgs__msg__TrajectoryPointMsg__Sequence__fini(teb_msgs__msg__TrajectoryPointMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      teb_msgs__msg__TrajectoryPointMsg__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

teb_msgs__msg__TrajectoryPointMsg__Sequence *
teb_msgs__msg__TrajectoryPointMsg__Sequence__create(size_t size)
{
  teb_msgs__msg__TrajectoryPointMsg__Sequence * array = (teb_msgs__msg__TrajectoryPointMsg__Sequence *)malloc(sizeof(teb_msgs__msg__TrajectoryPointMsg__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = teb_msgs__msg__TrajectoryPointMsg__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
teb_msgs__msg__TrajectoryPointMsg__Sequence__destroy(teb_msgs__msg__TrajectoryPointMsg__Sequence * array)
{
  if (array) {
    teb_msgs__msg__TrajectoryPointMsg__Sequence__fini(array);
  }
  free(array);
}

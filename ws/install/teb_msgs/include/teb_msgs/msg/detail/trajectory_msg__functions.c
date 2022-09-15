// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from teb_msgs:msg/TrajectoryMsg.idl
// generated code does not contain a copyright notice
#include "teb_msgs/msg/detail/trajectory_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `trajectory`
#include "teb_msgs/msg/detail/trajectory_point_msg__functions.h"

bool
teb_msgs__msg__TrajectoryMsg__init(teb_msgs__msg__TrajectoryMsg * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    teb_msgs__msg__TrajectoryMsg__fini(msg);
    return false;
  }
  // trajectory
  if (!teb_msgs__msg__TrajectoryPointMsg__Sequence__init(&msg->trajectory, 0)) {
    teb_msgs__msg__TrajectoryMsg__fini(msg);
    return false;
  }
  return true;
}

void
teb_msgs__msg__TrajectoryMsg__fini(teb_msgs__msg__TrajectoryMsg * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // trajectory
  teb_msgs__msg__TrajectoryPointMsg__Sequence__fini(&msg->trajectory);
}

teb_msgs__msg__TrajectoryMsg *
teb_msgs__msg__TrajectoryMsg__create()
{
  teb_msgs__msg__TrajectoryMsg * msg = (teb_msgs__msg__TrajectoryMsg *)malloc(sizeof(teb_msgs__msg__TrajectoryMsg));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(teb_msgs__msg__TrajectoryMsg));
  bool success = teb_msgs__msg__TrajectoryMsg__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
teb_msgs__msg__TrajectoryMsg__destroy(teb_msgs__msg__TrajectoryMsg * msg)
{
  if (msg) {
    teb_msgs__msg__TrajectoryMsg__fini(msg);
  }
  free(msg);
}


bool
teb_msgs__msg__TrajectoryMsg__Sequence__init(teb_msgs__msg__TrajectoryMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  teb_msgs__msg__TrajectoryMsg * data = NULL;
  if (size) {
    data = (teb_msgs__msg__TrajectoryMsg *)calloc(size, sizeof(teb_msgs__msg__TrajectoryMsg));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = teb_msgs__msg__TrajectoryMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        teb_msgs__msg__TrajectoryMsg__fini(&data[i - 1]);
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
teb_msgs__msg__TrajectoryMsg__Sequence__fini(teb_msgs__msg__TrajectoryMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      teb_msgs__msg__TrajectoryMsg__fini(&array->data[i]);
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

teb_msgs__msg__TrajectoryMsg__Sequence *
teb_msgs__msg__TrajectoryMsg__Sequence__create(size_t size)
{
  teb_msgs__msg__TrajectoryMsg__Sequence * array = (teb_msgs__msg__TrajectoryMsg__Sequence *)malloc(sizeof(teb_msgs__msg__TrajectoryMsg__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = teb_msgs__msg__TrajectoryMsg__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
teb_msgs__msg__TrajectoryMsg__Sequence__destroy(teb_msgs__msg__TrajectoryMsg__Sequence * array)
{
  if (array) {
    teb_msgs__msg__TrajectoryMsg__Sequence__fini(array);
  }
  free(array);
}

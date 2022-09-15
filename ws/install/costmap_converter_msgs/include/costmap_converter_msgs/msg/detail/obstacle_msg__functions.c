// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from costmap_converter_msgs:msg/ObstacleMsg.idl
// generated code does not contain a copyright notice
#include "costmap_converter_msgs/msg/detail/obstacle_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `polygon`
#include "geometry_msgs/msg/detail/polygon__functions.h"
// Member `orientation`
#include "geometry_msgs/msg/detail/quaternion__functions.h"
// Member `velocities`
#include "geometry_msgs/msg/detail/twist_with_covariance__functions.h"

bool
costmap_converter_msgs__msg__ObstacleMsg__init(costmap_converter_msgs__msg__ObstacleMsg * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    costmap_converter_msgs__msg__ObstacleMsg__fini(msg);
    return false;
  }
  // polygon
  if (!geometry_msgs__msg__Polygon__init(&msg->polygon)) {
    costmap_converter_msgs__msg__ObstacleMsg__fini(msg);
    return false;
  }
  // radius
  // id
  // orientation
  if (!geometry_msgs__msg__Quaternion__init(&msg->orientation)) {
    costmap_converter_msgs__msg__ObstacleMsg__fini(msg);
    return false;
  }
  // velocities
  if (!geometry_msgs__msg__TwistWithCovariance__init(&msg->velocities)) {
    costmap_converter_msgs__msg__ObstacleMsg__fini(msg);
    return false;
  }
  return true;
}

void
costmap_converter_msgs__msg__ObstacleMsg__fini(costmap_converter_msgs__msg__ObstacleMsg * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // polygon
  geometry_msgs__msg__Polygon__fini(&msg->polygon);
  // radius
  // id
  // orientation
  geometry_msgs__msg__Quaternion__fini(&msg->orientation);
  // velocities
  geometry_msgs__msg__TwistWithCovariance__fini(&msg->velocities);
}

costmap_converter_msgs__msg__ObstacleMsg *
costmap_converter_msgs__msg__ObstacleMsg__create()
{
  costmap_converter_msgs__msg__ObstacleMsg * msg = (costmap_converter_msgs__msg__ObstacleMsg *)malloc(sizeof(costmap_converter_msgs__msg__ObstacleMsg));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(costmap_converter_msgs__msg__ObstacleMsg));
  bool success = costmap_converter_msgs__msg__ObstacleMsg__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
costmap_converter_msgs__msg__ObstacleMsg__destroy(costmap_converter_msgs__msg__ObstacleMsg * msg)
{
  if (msg) {
    costmap_converter_msgs__msg__ObstacleMsg__fini(msg);
  }
  free(msg);
}


bool
costmap_converter_msgs__msg__ObstacleMsg__Sequence__init(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  costmap_converter_msgs__msg__ObstacleMsg * data = NULL;
  if (size) {
    data = (costmap_converter_msgs__msg__ObstacleMsg *)calloc(size, sizeof(costmap_converter_msgs__msg__ObstacleMsg));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = costmap_converter_msgs__msg__ObstacleMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        costmap_converter_msgs__msg__ObstacleMsg__fini(&data[i - 1]);
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
costmap_converter_msgs__msg__ObstacleMsg__Sequence__fini(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      costmap_converter_msgs__msg__ObstacleMsg__fini(&array->data[i]);
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

costmap_converter_msgs__msg__ObstacleMsg__Sequence *
costmap_converter_msgs__msg__ObstacleMsg__Sequence__create(size_t size)
{
  costmap_converter_msgs__msg__ObstacleMsg__Sequence * array = (costmap_converter_msgs__msg__ObstacleMsg__Sequence *)malloc(sizeof(costmap_converter_msgs__msg__ObstacleMsg__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = costmap_converter_msgs__msg__ObstacleMsg__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
costmap_converter_msgs__msg__ObstacleMsg__Sequence__destroy(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array)
{
  if (array) {
    costmap_converter_msgs__msg__ObstacleMsg__Sequence__fini(array);
  }
  free(array);
}

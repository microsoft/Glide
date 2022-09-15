// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from costmap_converter_msgs:msg/ObstacleMsg.idl
// generated code does not contain a copyright notice

#ifndef COSTMAP_CONVERTER_MSGS__MSG__DETAIL__OBSTACLE_MSG__FUNCTIONS_H_
#define COSTMAP_CONVERTER_MSGS__MSG__DETAIL__OBSTACLE_MSG__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "costmap_converter_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "costmap_converter_msgs/msg/detail/obstacle_msg__struct.h"

/// Initialize msg/ObstacleMsg message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * costmap_converter_msgs__msg__ObstacleMsg
 * )) before or use
 * costmap_converter_msgs__msg__ObstacleMsg__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
bool
costmap_converter_msgs__msg__ObstacleMsg__init(costmap_converter_msgs__msg__ObstacleMsg * msg);

/// Finalize msg/ObstacleMsg message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
void
costmap_converter_msgs__msg__ObstacleMsg__fini(costmap_converter_msgs__msg__ObstacleMsg * msg);

/// Create msg/ObstacleMsg message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * costmap_converter_msgs__msg__ObstacleMsg__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
costmap_converter_msgs__msg__ObstacleMsg *
costmap_converter_msgs__msg__ObstacleMsg__create();

/// Destroy msg/ObstacleMsg message.
/**
 * It calls
 * costmap_converter_msgs__msg__ObstacleMsg__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
void
costmap_converter_msgs__msg__ObstacleMsg__destroy(costmap_converter_msgs__msg__ObstacleMsg * msg);


/// Initialize array of msg/ObstacleMsg messages.
/**
 * It allocates the memory for the number of elements and calls
 * costmap_converter_msgs__msg__ObstacleMsg__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
bool
costmap_converter_msgs__msg__ObstacleMsg__Sequence__init(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array, size_t size);

/// Finalize array of msg/ObstacleMsg messages.
/**
 * It calls
 * costmap_converter_msgs__msg__ObstacleMsg__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
void
costmap_converter_msgs__msg__ObstacleMsg__Sequence__fini(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array);

/// Create array of msg/ObstacleMsg messages.
/**
 * It allocates the memory for the array and calls
 * costmap_converter_msgs__msg__ObstacleMsg__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
costmap_converter_msgs__msg__ObstacleMsg__Sequence *
costmap_converter_msgs__msg__ObstacleMsg__Sequence__create(size_t size);

/// Destroy array of msg/ObstacleMsg messages.
/**
 * It calls
 * costmap_converter_msgs__msg__ObstacleMsg__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costmap_converter_msgs
void
costmap_converter_msgs__msg__ObstacleMsg__Sequence__destroy(costmap_converter_msgs__msg__ObstacleMsg__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // COSTMAP_CONVERTER_MSGS__MSG__DETAIL__OBSTACLE_MSG__FUNCTIONS_H_

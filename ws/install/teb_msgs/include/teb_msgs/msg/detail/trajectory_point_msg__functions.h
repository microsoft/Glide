// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from teb_msgs:msg/TrajectoryPointMsg.idl
// generated code does not contain a copyright notice

#ifndef TEB_MSGS__MSG__DETAIL__TRAJECTORY_POINT_MSG__FUNCTIONS_H_
#define TEB_MSGS__MSG__DETAIL__TRAJECTORY_POINT_MSG__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "teb_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "teb_msgs/msg/detail/trajectory_point_msg__struct.h"

/// Initialize msg/TrajectoryPointMsg message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * teb_msgs__msg__TrajectoryPointMsg
 * )) before or use
 * teb_msgs__msg__TrajectoryPointMsg__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
bool
teb_msgs__msg__TrajectoryPointMsg__init(teb_msgs__msg__TrajectoryPointMsg * msg);

/// Finalize msg/TrajectoryPointMsg message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
void
teb_msgs__msg__TrajectoryPointMsg__fini(teb_msgs__msg__TrajectoryPointMsg * msg);

/// Create msg/TrajectoryPointMsg message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * teb_msgs__msg__TrajectoryPointMsg__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
teb_msgs__msg__TrajectoryPointMsg *
teb_msgs__msg__TrajectoryPointMsg__create();

/// Destroy msg/TrajectoryPointMsg message.
/**
 * It calls
 * teb_msgs__msg__TrajectoryPointMsg__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
void
teb_msgs__msg__TrajectoryPointMsg__destroy(teb_msgs__msg__TrajectoryPointMsg * msg);


/// Initialize array of msg/TrajectoryPointMsg messages.
/**
 * It allocates the memory for the number of elements and calls
 * teb_msgs__msg__TrajectoryPointMsg__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
bool
teb_msgs__msg__TrajectoryPointMsg__Sequence__init(teb_msgs__msg__TrajectoryPointMsg__Sequence * array, size_t size);

/// Finalize array of msg/TrajectoryPointMsg messages.
/**
 * It calls
 * teb_msgs__msg__TrajectoryPointMsg__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
void
teb_msgs__msg__TrajectoryPointMsg__Sequence__fini(teb_msgs__msg__TrajectoryPointMsg__Sequence * array);

/// Create array of msg/TrajectoryPointMsg messages.
/**
 * It allocates the memory for the array and calls
 * teb_msgs__msg__TrajectoryPointMsg__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
teb_msgs__msg__TrajectoryPointMsg__Sequence *
teb_msgs__msg__TrajectoryPointMsg__Sequence__create(size_t size);

/// Destroy array of msg/TrajectoryPointMsg messages.
/**
 * It calls
 * teb_msgs__msg__TrajectoryPointMsg__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_teb_msgs
void
teb_msgs__msg__TrajectoryPointMsg__Sequence__destroy(teb_msgs__msg__TrajectoryPointMsg__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // TEB_MSGS__MSG__DETAIL__TRAJECTORY_POINT_MSG__FUNCTIONS_H_

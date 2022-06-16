// Copyright 2022 AxelYoung (@AxelYoung)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#define USE_SERIAL
#define SOFT_SERIAL_PIN D1
#define MASTER_LEFT

#define MATRIX_ROW 4
#define MATRIX_COL 10
#define MATRIX_ROW_PINS { D7, E6, B4, B5 }
#define MATRIX_COL_PINS { F7, B1, B3, B2, B6 }

#define MATRIX_ROW_PINS_RIGHT { B1, B3, B2, B6 }
#define MATRIX_COL_PINS_RIGHT { C6, D7, E6, B4, B5 }

#define ENCODERS_PAD_A { D0 }
#define ENCODERS_PAD_B { D4 }

#define DIP_SWITCH_PINS { C6 }
#define DIP_SWITCH_PINS_RIGHT { F7 }

#ifdef JOYSTICK_ENABLE
  #define JOYSTICK_BUTTON_COUNT 0
  #define JOYSTICK_AXES_COUNT 2
  #define JOYSTICK_AXES_RESOLUTION 10
#endif

#define ANALOG_JOYSTICK_X_AXIS_PIN F5
#define ANALOG_JOYSTICK_Y_AXIS_PIN F6
#define POINTING_DEVICE_INVERT_X 
#define ANALOG_JOYSTICK_SPEED_REGULATOR 30

#ifdef ENCODER_ENABLE
#    define ENCODER_DIRECTION_FLIP
#    define ENCODER_RESOLUTION 2
#endif

#ifdef THUMBSTICK_ENABLE
#    define THUMBSTICK_FLIP_X
#    define THUMBSTICK_PIN_X F5
#    define THUMBSTICK_PIN_Y F6
#endif

/*
 * Feature disable options
 *  These options are also useful to firmware size reduction.
 */

/* disable debug print */
//#define NO_DEBUG

/* disable print */
//#define NO_PRINT

/* disable action features */
//#define NO_ACTION_LAYER
//#define NO_ACTION_TAPPING
//#define NO_ACTION_ONESHOT

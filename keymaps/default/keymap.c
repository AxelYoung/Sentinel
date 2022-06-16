#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_split_3x5_2(
        KC_Q,    KC_D,    KC_R,    KC_W,    KC_B,                               KC_J,    KC_F,    KC_U,    KC_P,    KC_SEMICOLON,
        KC_A,    KC_S,    KC_H,    KC_T,    KC_G,                               KC_Y,    KC_N,    KC_E,    KC_O,    KC_I,
        KC_Z,    KC_X,    KC_M,    KC_C,    KC_V,                               KC_K,    KC_L,    KC_COMM, KC_DOT,  KC_SLSH,
        KC_LEFT_CTRL,    MO(1),             KC_LEFT_SHIFT, KC_SPC,                        KC_BACKSPACE,  KC_LEFT_SHIFT, KC_P,  LT(2, KC_ENTER)  
    ),

    [1] = LAYOUT_split_3x5_2(
        KC_1,    KC_2,    KC_3,    KC_4,    KC_5,                               KC_6,    KC_7,    KC_8,    KC_9,    KC_0,
        KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,                          KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,
        KC_ESCAPE,    KC_CAPS_LOCK,    KC_LEFT_GUI,    KC_QUOTE,    KC_V,                               KC_LEFT_BRACKET,    KC_LEFT_BRACKET,    KC_BACKSLASH, KC_F11,  KC_F12,
        KC_LEFT_CTRL,    KC_NO,             KC_LEFT_SHIFT, KC_SPC,                        KC_BACKSPACE,  KC_LEFT_SHIFT, KC_P, KC_ENTER
    ),

    [2] = LAYOUT_split_3x5_2(
        KC_Q,    KC_D,    KC_R,    KC_W,    KC_B,                               KC_J,    KC_F,    KC_U,    KC_P,    KC_SEMICOLON,
        KC_A,    KC_S,    KC_H,    KC_T,    KC_G,                               KC_Y,    KC_BTN1,    KC_BTN2,    KC_O,    KC_I,
        KC_Z,    KC_X,    KC_M,    KC_C,    KC_V,                               KC_K,    KC_L,    KC_COMM, KC_DOT,  KC_SLSH,
        KC_LEFT_CTRL,    KC_NO,             KC_LEFT_SHIFT, KC_SPC,                        KC_BACKSPACE,  KC_LEFT_SHIFT, KC_P,  LT(2, KC_ENTER)  
    )
};

bool encoder_update_user(uint8_t index, bool clockwise) {
    if (index == 0) { /* First encoder */
        if (clockwise) {
            tap_code_delay(KC_VOLU, 10);
        } else {
            tap_code_delay(KC_VOLD, 10);
        }
    } else if (index == 1) {
        if (clockwise) {
            tap_code16(C(KC_Y));
        } else {
            tap_code16(C(KC_Z));
        }
    }
    return false;
}

bool dip_switch_update_user(uint8_t index, bool active) { 
    switch (index) {
        case 0:	
            if(active) { 
			    tap_code16(KC_MUTE);
		    } 
            break;
        case 1:	
            if(active) { 
			    tap_code16(C(KC_S));
		    } 
            break;
	}
    return true;
}
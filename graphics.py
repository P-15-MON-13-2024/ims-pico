import framebuf
wifi_connected_symbol_8x16 = bytearray([
    0b11111111, 0b00000000,
    0b00000000, 0b00000000,
    0b01111110, 0b00000000,
    0b00000000, 0b00000000,
    0b00111100, 0b10100000,
    0b00000000, 0b10110000,
    0b00011001, 0b10100000,
    0b00000000, 0b10100000,
])
wifi_connected_symbol_8x16_fb = framebuf.FrameBuffer(wifi_connected_symbol_8x16, 16, 8, framebuf.MONO_HLSB)

wifi_lost_symbol_8x16 = bytearray([
    0b11111111, 0b00000000,
    0b00000000, 0b00000000,
    0b01111110, 0b00000000,
    0b00000001, 0b00010000,
    0b00111100, 0b10100000,
    0b00000000, 0b01000000,
    0b00011000, 0b10100000,
    0b00000001, 0b00010000,
])
wifi_lost_symbol_8x16_fb = framebuf.FrameBuffer(wifi_lost_symbol_8x16, 16, 8, framebuf.MONO_HLSB)

wifi_download_symbol_8x16 = bytearray([
    0b11111111, 0b00000000,
    0b00000000, 0b00000000,
    0b01111110, 0b00000000,
    0b00000000, 0b01000000,
    0b00111100, 0b01000000,
    0b00000001, 0b01010000,
    0b00011000, 0b11100000,
    0b00000000, 0b01000000,
])
wifi_download_symbol_8x16_fb = framebuf.FrameBuffer(wifi_download_symbol_8x16, 16, 8, framebuf.MONO_HLSB)

wifi_upload_symbol_8x16 = bytearray([
    0b11111111, 0b00000000,
    0b00000000, 0b00000000,
    0b01111110, 0b00000000,
    0b00000000, 0b01000000,
    0b00111100, 0b11100000,
    0b00000001, 0b01010000,
    0b00011000, 0b01000000,
    0b00000000, 0b01000000,
])
wifi_upload_symbol_8x16_fb = framebuf.FrameBuffer(wifi_upload_symbol_8x16, 16, 8, framebuf.MONO_HLSB)

option_picker_8x8 = bytearray([
    0b00011000,
    0b00111100,
    0b01111100,
    0b11111100,
    0b11111100,
    0b01111100,
    0b00111100,
    0b00011000,
    
])
option_picker_8x8_fb = framebuf.FrameBuffer(option_picker_8x8, 8, 8, framebuf.MONO_HLSB)

battery_0_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00100000, 0b00000001,
    0b11100000, 0b00000001,
    0b11100000, 0b00000001,
    0b00100000, 0b00000001,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_0_8x16_fb = framebuf.FrameBuffer(battery_0_8x16, 16, 8, framebuf.MONO_HLSB)

battery_1_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00100000, 0b00001101,
    0b11100000, 0b00001101,
    0b11100000, 0b00001101,
    0b00100000, 0b00001101,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_1_8x16_fb = framebuf.FrameBuffer(battery_1_8x16, 16, 8, framebuf.MONO_HLSB)

battery_2_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00100000, 0b00111101,
    0b11100000, 0b00111101,
    0b11100000, 0b00111101,
    0b00100000, 0b00111101,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_2_8x16_fb = framebuf.FrameBuffer(battery_2_8x16, 16, 8, framebuf.MONO_HLSB)

battery_3_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00100000, 0b11111101,
    0b11100000, 0b11111101,
    0b11100000, 0b11111101,
    0b00100000, 0b11111101,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_3_8x16_fb = framebuf.FrameBuffer(battery_3_8x16, 16, 8, framebuf.MONO_HLSB)

battery_4_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00100011, 0b11111101,
    0b11100011, 0b11111101,
    0b11100011, 0b11111101,
    0b00100011, 0b11111101,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_4_8x16_fb = framebuf.FrameBuffer(battery_4_8x16, 16, 8, framebuf.MONO_HLSB)

battery_5_8x16 = bytearray([
    0b00111111, 0b11111111,
    0b00100000, 0b00000001,
    0b00101111, 0b11111101,
    0b11101111, 0b11111101,
    0b11101111, 0b11111101,
    0b00101111, 0b11111101,
    0b00100000, 0b00000001,
    0b00111111, 0b11111111,
])
battery_5_8x16_fb = framebuf.FrameBuffer(battery_5_8x16, 16, 8, framebuf.MONO_HLSB)


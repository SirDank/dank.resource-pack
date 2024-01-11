#version 150

#define PI (3.1415926538)
#define EDGE_BRIGHTNESS (0.5)

float edginess(vec2 uv) {
    return (1 - EDGE_BRIGHTNESS) + sin(PI * uv.x) * sin(PI * uv.y) * EDGE_BRIGHTNESS;
}

const vec2 DefaultUVs[4] = vec2[](vec2(1, 0), vec2(0, 0), vec2(0, 1), vec2(1, 1));

#version 150

vec2 discretize(vec2 pos, vec2 size) {
    pos *= size;
    pos = floor(pos);
    pos /= size;
    return pos;
}

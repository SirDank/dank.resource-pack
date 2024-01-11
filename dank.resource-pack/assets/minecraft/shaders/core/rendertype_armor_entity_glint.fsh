#version 150

#moj_import <fog.glsl>
#moj_import <discretize.glsl>
#moj_import <glint.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform float GlintAlpha;

uniform mat4 TextureMat;

in float vertexDistance;
in vec2 texCoord0;

in vec2 edgeUV;

out vec4 fragColor;

void main() {
    vec2 texCoord0 = discretize(texCoord0, vec2(64, 32));
    texCoord0 = (TextureMat * vec4(texCoord0, 0, 1)).xy;
    vec4 color = texture(Sampler0, texCoord0) * ColorModulator;
    
    color = floor(color * 8) / 8;
    float edge = edginess(edgeUV);
    color /= edge * edge * edge * edge * 7;
    
    if (color.a < 0.1) {
        discard;
    }
    
    float fade = linear_fog_fade(vertexDistance, FogStart, FogEnd) * GlintAlpha;
    fragColor = vec4(color.rgb * fade, color.a);
}

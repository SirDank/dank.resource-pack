#version 150

#moj_import <fog.glsl>
#moj_import <glint.glsl>

in vec3 Position;
in vec2 UV0;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform mat4 TextureMat;
uniform int FogShape;

out float vertexDistance;
out vec2 texCoord0;

out vec2 edgeUV;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    
    vertexDistance = fog_distance(ModelViewMat, Position, FogShape);
    texCoord0 = UV0;
    
    // equivalent to gl_VertexID % 4 (thanks /u/Mudkip-Mudkip-Mudkip!)
    int vertIndex = gl_VertexID & 3;
    edgeUV = DefaultUVs[vertIndex];
}

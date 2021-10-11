#define MAX_LIGHTS 5

attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

// uniform vec4 u_color;
// Global coordinates

uniform vec4 u_eye_position;

uniform vec4 u_light_position[MAX_LIGHTS];
uniform int u_number_of_lights;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying float v_l[2];

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// local coordinates
	position = u_model_matrix * position;
	v_normal = u_model_matrix * normal;

	// global coordinates
	vec4 v = u_eye_position - position;
	vec4 closest = u_light_position[0] - position;
	v_l[0] = 0.0;
	for (int i = 0; i < u_number_of_lights; i++){
		vec4 pos = u_light_position[i] - position;
		if (length(pos) < length(closest)) {
			closest = pos;
			v_l[1] = v_l[0];
			v_l[0] = float(i);
		}
	}
	// v_s = u_light_position[i] - position;
	v_s = closest;
	v_h = v_s+v;

	// float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	// float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	// v_color = (light_factor_1 + light_factor_2) * u_color;

	// ### --- Change the projection_view_matrix to separate view and projection matrices --- ### 
	position = u_view_matrix * position;
	//eye coordinates
	position = u_projection_matrix * position;
	// clip coordinates

	gl_Position = position;
}
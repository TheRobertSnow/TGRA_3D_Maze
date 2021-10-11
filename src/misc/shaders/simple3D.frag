#define MAX_LIGHTS 5

uniform vec4 u_light_diffuse[MAX_LIGHTS];
uniform vec4 u_light_specular[MAX_LIGHTS];
uniform vec4 u_light_ambient[MAX_LIGHTS];
uniform int u_number_of_lights;
uniform vec4 u_directional_light;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform vec4 u_mat_ambient;
uniform float u_mat_shininess;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying float v_l[2];

void main(void)
{
	vec4 v_color = vec4(0.0, 0.0, 0.0, 0.0);
	// vec4 v_color;
	for (int i = 0; i < 2; i++){
		float lambert = max(dot(normalize(v_normal), normalize(v_s)), 0.0);
		float phong = max(dot(normalize(v_normal), normalize(v_h)), 0.0);
		v_color += (u_light_diffuse[int(v_l[i])] * u_mat_diffuse * lambert
				+ u_light_specular[int(v_l[i])] * u_mat_specular * pow(phong, u_mat_shininess))
				+ u_directional_light * u_mat_ambient;

	}
	gl_FragColor = v_color;
}
import sys
from PIL import Image
import numpy as np

def solve_transformation(p, q):
	a = np.array([
		[ p[0][0], p[0][1], p[0][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   -q[0][0], 0, 	   0,        0        ],
		[ 0, 	   0, 		0, 		 p[0][0], p[0][1], p[0][2], 0, 		 0, 	  0, 	   -q[0][1], 0, 	   0, 	     0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[0][0], p[0][1], p[0][2], -q[0][2], 0, 	   0,        0        ],

		[ p[1][0], p[1][1], p[1][2], 0, 	  0, 	   0, 	 	0, 		 0, 	  0, 	   0, 		 -q[1][0], 0, 	     0        ],
		[ 0, 	   0, 		0, 		 p[1][0], p[1][1], p[1][2], 0, 		 0, 	  0, 	   0, 		 -q[1][1], 0, 	     0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[1][0], p[1][1], p[1][2], 0, 		 -q[1][2], 0, 	     0        ],

		[ p[2][0], p[2][1], p[2][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 0, 	   -q[2][0], 0        ],
		[ 0, 	   0, 		0, 		 p[2][0], p[2][1], p[2][2], 0, 		 0, 	  0, 	   0, 		 0, 	   -q[2][1], 0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[2][0], p[2][1], p[2][2], 0, 		 0, 	   -q[2][2], 0        ],

		[ p[3][0], p[3][1], p[3][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 0, 	   0, 	     -q[3][0] ],
		[ 0, 	   0,		0,	 	 p[3][0], p[3][1], p[3][2], 0, 		 0, 	  0, 	   0, 		 0, 	   0, 	     -q[3][1] ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[3][0], p[3][1], p[3][2], 0, 		 0, 	   0, 	     -q[3][2] ],

		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   1, 		 0, 	   0, 	    0 ]
	])

	b = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

	x = np.linalg.solve(a, b)
	return np.linalg.inv(np.array([
		[x[0], x[1], x[2]],
		[x[3], x[4], x[5]],
		[x[6], x[7], x[8]]
	]))

def texture_color(x, y, w, h, c):
	return c[round(x) % w, -round(y) % h]

if __name__ == "__main__":
	if len(sys.argv) < 11: 
		print("numero de parametros errados")
		exit()

	texture = Image.open(sys.argv[1])
	original = Image.open(sys.argv[2])

	texture_width, texture_height = texture.size
	texture_colors = texture.load()

	orig_width, orig_height = original.size

	texture_points = [
		[0,texture_height-1,1],
		[texture_width-1,texture_height-1,1],
		[texture_width-1,0,1],
		[0,0,1],
	]

	original_points = []
	for i in range(4):
		original_points.append([int(sys.argv[3+2*i]), int(sys.argv[4+2*i]), 1])
		print(original_points[i], "->", texture_points[i])

	# transformation matrix
	tranformation = solve_transformation(texture_points, original_points)

	# iterate over all pixels of original image
	for x_orig in range(orig_width):
		for y_orig in range(orig_height):
			original_point = (x_orig, y_orig, 1) # RP2

			# corresponding point in texture
			texture_point = np.dot(tranformation, original_point) # RP2
			x_texture = texture_point[0]/texture_point[2]
			y_texture = texture_point[1]/texture_point[2] 

			# if inside texture rectangle apply color
			if 0 < x_texture and x_texture < texture_width and 0 < y_texture and y_texture < texture_height:
				original.putpixel(
					(x_orig,y_orig), 
					texture_color(x_texture, y_texture, texture_width, texture_height, texture_colors)
				)

	if len(sys.argv) == 12:
		original.save(sys.argv[3])
	else:
		original.save("result.png")

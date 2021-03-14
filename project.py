import sys
import numpy as np
from PIL import Image

def solve_transformation(p, q):
	a = np.array([
		[ p[0][0], p[0][1], p[0][2], 0, 	  0, 	   0, 		0, 		0, 		0, 		   0, 		 0, 	   0        ],
		[ 0, 	   0, 		0, 		 p[0][0], p[0][1], p[0][2], 0, 		0, 		0, 		   0, 		 0, 	   0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[0][0], p[0][1], p[0][2], 0, 		 0,    	   0        ],

		[ p[1][0], p[1][1], p[1][2], 0, 	  0, 	   0, 	 	0, 		 0, 	  0, 	   -q[1][0], 0, 	   0        ],
		[ 0, 	   0, 		0, 		 p[1][0], p[1][1], p[1][2], 0, 		 0, 	  0, 	   -q[1][1], 0, 	   0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[1][0], p[1][1], p[1][2], -q[1][2], 0, 	   0        ],

		[ p[2][0], p[2][1], p[2][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 -q[2][0], 0        ],
		[ 0, 	   0, 		0, 		 p[2][0], p[2][1], p[2][2], 0, 		 0, 	  0, 	   0, 	     -q[2][1], 0        ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[2][0], p[2][1], p[2][2], 0, 		 -q[2][2], 0        ],

		[ p[3][0], p[3][1], p[3][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 0, 	   -q[3][0] ],
		[ 0, 	   0,		0,	 	 p[3][0], p[3][1], p[3][2], 0, 		 0, 	  0, 	   0, 		 0, 	   -q[3][1] ],
		[ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		p[3][0], p[3][1], p[3][2], 0, 		 0, 	   -q[3][2] ]
	])

	b = np.array([q[0][0], q[0][1], q[0][2], 0, 0, 0, 0, 0, 0, 0, 0, 0])

	x = np.linalg.solve(a, b)
	return np.linalg.inv(np.array([
		[x[0], x[1], x[2]],
		[x[3], x[4], x[5]],
		[x[6], x[7], x[8]]
	]))

def is_inside(x, y, w, h):
	return 

def texture_color(x, y, w, h, c):
	return c[round(x) % w, -round(y) % h]

if __name__ == "__main__":
	if len(sys.argv) < 11: 
		print("numero de parametros errados")
		exit()

	texture = Image.open(sys.argv[1])
	original = Image.open(sys.argv[2])

	wT, hT = texture.size
	cT = texture.load()

	wO, hO = original.size
	cO = original.load()

	p = [
		[0,hT-1,1],
		[wT-1,hT-1,1],
		[wT-1,0,1],
		[0,0,1],
	]

	q = []
	for i in range(4):
		q.append([int(sys.argv[3+2*i]), int(sys.argv[4+2*i]), 1])

	# transformation matrix
	tranformation = solve_transformation(p, q)

	# iterate over all pixels of original image
	for xO in range(wO):
		for yO in range(hO):
			original_point = (xO, yO, 1) # RP2

			# corresponding point in texture
			texture_point = np.dot(tranformation, original_point) # RP2
			xT = texture_point[0]/texture_point[2]
			yT = texture_point[1]/texture_point[2] 

			# if inside texture rectangle apply color
			if 0 < xT and xT < wT and 0 < yT and yT < hT:
				original.putpixel(
					(xO,yO), 
					texture_color(xT, yT, wT, hT, cT)
				)

	if len(sys.argv) == 12:
		original.save(sys.argv[3])
	else:
		original.save("result.png")

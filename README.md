This code conducts automated image processing to identify and count particles in images. 
Initially, it loads images from a main directory and subdirectories for green and red colors. 
For each image, a threshold is applied to isolate the particles, and contours are drawn around them. 
If the particle count in an image exceeds a certain threshold, another threshold is applied. 
Finally, the processed images with marked particles are saved, and the count of particles in each image is outputted.

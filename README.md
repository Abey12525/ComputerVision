# <center>Occlusions In Stereo Vision</center>
***
## Types of Occlusions 
### Border Occlusion
Occlusions that occur near the image borders are called border occlusions. Border occlusions in the left image occur due to the right camera missing some of the left portion of the field of view of the left camera.

### Non-Border Occlusion
Occlusions that appear inside the images when two or more distinct surfaces appear as foregrounds and backgrounds in the scene are called non-border occlusions. Parts of the background near the boundary of two surfaces become invisible

1) Partial Occlusion
    * In partial occlusions,only a part of a background surface become invisible to one camera

2) Self Occlusion
    * Portion of the visible foreground surface becomes invisible to one camera due to the curvature of the surface
    * Part of a continuous and curved surface is being occluded by another part of the same surface. 
    * If images of the curved surface lack gradients, the surface appears planar to binocular stereo, making detection of the occlusion impossible
3) Total Occlusion
    * An isolated scene surface visible to one camera becomes entirely invisible to the other camera.

Border Occlusion - Right-to-left 
Non-Border occlusion - left-to-right  

  
### Half Occlusion _(Occlusion shown only in one direction, left-to-right)_


We Obtain difference image by shifting the right image further to the right , and then subtracting the left
and the shifted right images. This is done for all disparities

A set of difference images is called 3-D cost volume $`e(p,d)`$,
where $p$ and $d$ represent the 2-D locations of pixels and disparity respectively.

We call the 3-D cost volume a per-pixel cost.
we define the per-pixel cost $e$ as 

  $`e(p,d) = E(p,d) + n `$  
  $`n = noise `$  
  $`E(p,d)\ is\ represented\ as\ E(p) `$

$E(p) :$  2-D cost function which is the section of 3-D cost volume, given the disparity value
of $d$.

## Asymmetric Occlusion Detection

"Asymmetric occlusion detection uses geometric and photometric constraints. To determine whether a pixel is visible or not, we have to evaluate the disparity values of the neighboring pixels. Since it is assumed that the epipolar line is parallel, we only consider the pixels in the corresponding horizontal line. In fact, to use ordering constraint means that only the right pixel of each pixel is considered. The disparity of the occluding pixels is generally larger than that of the occluded pixels" [2]

$` S_r(j) `$ - set of pixels in the right image  
$` S_r(j) = \{ i|i-d(i) = j, all\ i\ with\;\ 0 \le i \le W-1\}`$  
$`i, j`$ - x of coordinates left and right images respectively  
$W$ - width of the image  
$d$ - disparity of the pixel.  
$O_l$ - Visiblity function of left image, while takes the value __1__ when pixel is __visible__ and __0__ when __occluded__   
$E$ - Cost function  

**Asymmetric Occlusion Detection Using Geometric Constraints only:**  
  
$For\ each\ j, when \ (S_r(j))>1$  
&emsp; $Set\ i_m = arg\ max\ d(S_r(j)),\ i_o = S_r(j)-i_m$  
&emsp; $if\ i=i_m :$  
&emsp;&emsp; $O_l(i)=1$    
&emsp; $else:$  
&emsp;&emsp; $O_l(i)=0$  

**Asymmetric Occlusion Detection Using Geometric Constraints and Photometric Constraints:** 
  
$For\ each\ j, when \  (S_r(j))>1$  
&emsp;&emsp; $Set\ i_m = arg\ max\ d(S_r(j)),$  
&emsp;&emsp; $i_o = S_r(j)-i_m$  
&emsp;&emsp; $and \  i_n\ = arg\ min\ E(S_r(j),\ d(S_r(j)))$  

&emsp;&emsp; $if\ i_m=i_n :$  
&emsp;&emsp;&emsp;&emsp; $if\ i=i_m:$  
&emsp;&emsp;&emsp;&emsp;&emsp; $O_l(i)=1$  
&emsp;&emsp;&emsp;&emsp; $else$  
&emsp;&emsp;&emsp;&emsp;&emsp; $O_l(i)=0, for\ all\ i=i_o$  
&emsp;&emsp; $else:$  
&emsp;&emsp;&emsp;&emsp; $O_l(i)=0, for\ all\ i\in S_r(j)$  

\* All this visibility constraint requires is that an occluded pixel must have no
match on the other image and a non-occluded pixel must
have at least one match.[3]

\* A pixel in the left image will be visible in both images if there is at least one pixel in the right image matching it.

### Reference
[[1](https://www.sciencedirect.com/science/article/pii/S1077314213000155/pdfft?md5=06763e0bbc813b9c7021726b6b836c2a&pid=1-s2.0-S1077314213000155-main.pdf)]. Shafik Huq, Andreas Koschan, & Mongi Abidi (2013). Occlusion filling in stereo: Theory and experiments. Computer Vision and Image Understanding, 117(6), 688-704.

[[2](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4544568)]. Min, D., & Sohn, K. (2008). Cost Aggregation and Occlusion Handling With WLS in Stereo Matching. IEEE Transactions on Image Processing, 17(8), 1431-1442

[[3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/symmetricstereo_cvpr05.pdf)]. Sun, J., Li, Y., Kang, S.B. and Shum, H.Y. (2005) Symmetric Stereo Matching for Occlusion Handling. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2005), San Diego, CA, 20-26 June 2005, 399-406

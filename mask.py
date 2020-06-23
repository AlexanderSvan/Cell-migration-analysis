import cv2
from skimage.filters import difference_of_gaussians
import imutils
import numpy as np


def normalize(f):
   lmin = float(f.min())
   lmax = float(f.max())
   return np.floor((f-lmin)/(lmax-lmin)*255).astype('uint8')   



def mask_area(img, scale):
   
   class Map_coord():
   
      """CV2 class for storing left button clicks
                    
      Notes
      ----------
      Loads button clicks through cv2 and saves them in a list instantiated with the class
      
      """
      
      def __init__(self):
         self.points=[]
      
      def select_point(self,event,x,y,flags,param):
         if event == cv2.EVENT_LBUTTONDOWN:
             self.points.append([x,y])
             cv2.drawMarker(frame, (x,y), (0,0,0), markerType=cv2.MARKER_CROSS, markerSize=15, thickness=2)
             cv2.imshow("image", frame)
   

   
   #Instantiate class for getting button clicks
   coordinateStore = Map_coord()
   frame=normalize(difference_of_gaussians(img, 1, 5))
   frame = cv2.resize(frame, (0,0), fx=scale, fy=scale)
   cv2.imshow("image", frame)
   cv2.namedWindow("image")
   cv2.setMouseCallback("image", coordinateStore.select_point)
   
   while(1):
   	cv2.imshow('image',frame)
   	key = cv2.waitKey(1) & 0xFF
   	
   	if key == ord("q"):
   		break 
       
   cv2.destroyAllWindows()
   
   coords=[]
   
   for elements in coordinateStore.points:
       coords.append(list(elements)[::])
        
   for obj in coords:
      if obj in sorted(coords, key=lambda l: l[1])[:2]:
         obj[1]=0
      if obj in sorted(coords, key=lambda l: l[1])[-2:]:
         obj[1]=frame.shape[0]
       
   coords=[np.array(coords)]

   if len(coords[0])>4:
       stencil = np.zeros(frame.shape).astype(frame.dtype)
       color = [255, 255, 255]
       cv2.fillPoly(stencil, coords, color)   
       return imutils.resize(stencil, width=img.shape[1], height=img.shape[0])
 
   else:
       return None
   
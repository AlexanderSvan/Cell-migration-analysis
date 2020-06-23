from mask import mask_area
from skimage.filters import difference_of_gaussians, gaussian, threshold_otsu
from skimage.morphology import black_tophat, disk
import scipy.ndimage as ndi
from skimage.measure import regionprops
import csv
import nd2reader as nd2

class scratch:
   
   def __init__(self):
      self.img_set=None
      self.mask=[]
   
   def load(self, path):
      img=nd2.ND2Reader(path)
      img.bundle_axes='yx'
      img.default_coords['v'] = 1
      img.iter_axes='t'
      self.img_set=img
      self.pixes_size=self.img_set.metadata['pixel_microns']**2
      
   def set_freq(self, freq):
      self.freq=freq
   
   def mask_scratch(self):
      for v in range(self.img_set.sizes['v']):
         self.img_set.default_coords['v'] = v
         self.mask.append(mask_area(self.img_set[0], scale=0.25))
   
   def filter_size(self, min=0, max=9999):
      self.min_area=min
      self.max_area=max
   
   def analyse(self):
      all_wells=[]
      for well in range(self.img_set.sizes['v']):
         self.img_set.default_coords['v'] = well
         res=[]
         if self.mask[well] is not None:
            for img in self.img_set:
               passed=[]
               im=difference_of_gaussians(img, 1, 5)
               blur=gaussian(im, sigma=2)
               black=black_tophat(blur, selem=disk(4))
               thresh=threshold_otsu((black))
               black=black*self.mask[well].astype(bool).astype(int)
               objects=regionprops(ndi.label(black>thresh)[0])
               for obj in objects:
                  if obj.area>self.min_area and obj.area<self.max_area:
                     passed.append(obj.area)
               res.append(len(passed))
         else:
            res.append([])
         all_wells.append(res)
      with open("out.csv", "w", newline="") as f:
          writer = csv.writer(f)
          writer.writerows(res)




if __name__ == '__main__':
   
   test=scratch()
   test.load('/media/data/Scratch/Andreas_exp1_20200620.nd2')
   test.set_freq()
   test.mask_scratch()
   test.filter_size(min=20, max=200)
   res=test.analyse()

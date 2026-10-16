import unittest
from engineering_math import path_drop,interpolate,below_keel
class MathTests(unittest.TestCase):
 def test_distributed_load(self):
  self.assertAlmostEqual(path_drop([(10,.053,.5),(5,.053,.2)]),.636)
 def test_tank(self):
  self.assertEqual(interpolate([(0,0),(100,20),(200,60)],150),40)
  with self.assertRaises(ValueError):interpolate([(0,0),(100,20)],101)
  with self.assertRaises(ValueError):interpolate([(0,0),(0,20)],0)
 def test_depth(self):self.assertAlmostEqual(below_keel(4.2,.4,1.8),2.8)
 def test_invalid(self):
  with self.assertRaises(ValueError):path_drop([(10,.053,float('nan'))])
  with self.assertRaises(ValueError):below_keel(-1,0,0)
if __name__=='__main__':unittest.main()

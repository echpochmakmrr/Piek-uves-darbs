import unittest
import polygon as geom

neg_num = -42.0
rat_num = 15.0342842480


class TestPointStructure(unittest.TestCase):
    def test_default_constructor(self):
        p: geom.Point = geom.Point(0.0, 0.0)
        self.assertEqual(p.x, 0.0)
        self.assertEqual(p.y, 0.0)

    def test_arbitrary_constructor(self):
        p: geom.Point = geom.Point(neg_num, rat_num)
        self.assertEqual(p.x, neg_num)
        self.assertEqual(p.y, rat_num)

    def test_add(self):
        p_zero: geom.Point = geom.Point(0.0, 0.0)
        p: geom.Point = geom.Point(neg_num, rat_num)
        p = p+p_zero
        self.assertEqual(p.x, neg_num)
        self.assertEqual(p.y, rat_num)

    def test_sub(self):
        p1: geom.Point = geom.Point(neg_num, rat_num)
        p2: geom.Point = geom.Point(neg_num+1, rat_num+1)
        p1 = p2-p1
        self.assertEqual(p1.x, 1.0)
        self.assertEqual(p1.y, 1.0)

    def test_neg(self):
        p: geom.Point = geom.Point(-neg_num, -rat_num)
        p = -p
        self.assertEqual(p.x, neg_num)
        self.assertEqual(p.y, rat_num)


unittest.main()

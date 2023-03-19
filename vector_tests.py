import unittest
import polygon as geom

neg_num = -42.0
rat_num = 15.0342842480

zerop: geom.Point = geom.Point(0.0, 0.0)
randp: geom.Point = geom.Point(neg_num, rat_num)


class TestVectorStructure(unittest.TestCase):
    def test_nullvector_init(self):
        v: geom.Vector = geom.Vector(zerop)
        self.assertEqual(v.start.x, 0.0)
        self.assertEqual(v.start.y, 0.0)
        self.assertEqual(v.disp.x, 0.0)
        self.assertEqual(v.disp.y, 0.0)

    def test_nulldisplacement_init(self):
        v: geom.Vector = geom.Vector(zerop, randp)
        self.assertEqual(v.start.x, neg_num)
        self.assertEqual(v.start.y, rat_num)
        self.assertEqual(v.disp.x, 0.0)
        self.assertEqual(v.disp.y, 0.0)

    def test_nullstart_init(self):
        v: geom.Vector = geom.Vector(randp)
        self.assertEqual(v.start.x, 0.0)
        self.assertEqual(v.start.y, 0.0)
        self.assertEqual(v.disp.x, neg_num)
        self.assertEqual(v.disp.y, rat_num)

    def test_absolute_null(self):
        v: geom.Vector = geom.Vector(zerop)
        self.assertEqual(abs(v), 0.0)

    def test_absolute_around_origin(self):
        v: geom.Vector = geom.Vector(geom.Point(neg_num, rat_num), geom.Point(-neg_num/2, -rat_num/2))  # vector is split in half by origin
        self.assertAlmostEqual(abs(v), 44.6097, 4)

    def test_absolute_arbitrary(self):
        v: geom.Vector = geom.Vector(geom.Point(neg_num, rat_num))
        self.assertAlmostEqual(abs(v), 44.6097, 4)

    def test_add_null(self):
        v1: geom.Vector = geom.Vector(zerop)
        v2: geom.Vector = geom.Vector(zerop)
        v2 = v1+v2
        self.assertEqual(v2.disp.x, 0.0)
        self.assertEqual(v2.disp.y, 0.0)

    def test_add_opposing(self):
        v1: geom.Vector = geom.Vector(randp)
        v2: geom.Vector = geom.Vector(-randp)
        v2 = v1+v2
        self.assertEqual(v2.disp.x, 0.0)
        self.assertEqual(v2.disp.y, 0.0)

    def test_add_arbitrary(self):
        v1: geom.Vector = geom.Vector(geom.Point(rat_num*3, rat_num-12))
        v2: geom.Vector = geom.Vector(geom.Point(neg_num+4, rat_num))
        v2 = v1+v2
        self.assertEqual(v2.disp.x, (rat_num*3)+neg_num+4)
        self.assertEqual(v2.disp.y, (rat_num*2)-12)

    def test_sub_null(self):
        v1: geom.Vector = geom.Vector(zerop)
        v2: geom.Vector = geom.Vector(zerop)
        v2 = v1-v2
        self.assertEqual(v2.disp.x, 0.0)
        self.assertEqual(v2.disp.y, 0.0)

    def test_sub_opposing(self):
        v1: geom.Vector = geom.Vector(randp)
        v2: geom.Vector = geom.Vector(-randp)
        v2 = v1-v2
        self.assertEqual(v2.disp.x, 2*randp.x)
        self.assertEqual(v2.disp.y, 2*randp.y)

    def test_sub_arbitrary(self):
        v1: geom.Vector = geom.Vector(geom.Point(rat_num*3, rat_num-12))
        v2: geom.Vector = geom.Vector(geom.Point(neg_num+4, rat_num))
        v2 = v1-v2
        self.assertEqual(v2.disp.x, (rat_num*3)-neg_num-4)
        self.assertEqual(v2.disp.y, -12)

    def test_mul_null(self):
        v1: geom.Vector = geom.Vector(zerop)
        v2: geom.Vector = geom.Vector(zerop)
        res = v1*v2
        self.assertEqual(res, 0.0)

    def test_mul_null_and_arbitrary(self):
        v1: geom.Vector = geom.Vector(randp)
        v2: geom.Vector = geom.Vector(zerop)
        res = v1*v2
        self.assertEqual(res, 0.0)

    def test_mul_arbitrary(self):
        v1: geom.Vector = geom.Vector(geom.Point(rat_num*3, rat_num-12))
        v2: geom.Vector = geom.Vector(geom.Point(neg_num+4, rat_num))
        res = v1*v2
        self.assertEqual(res, (rat_num*3)*(neg_num+4)+(rat_num-12)*(rat_num))

    def test_xor_null(self):
        v1: geom.Vector = geom.Vector(zerop)
        v2: geom.Vector = geom.Vector(zerop)
        res = v1 ^ v2
        self.assertEqual(res, 0.0)

    def test_xor_null_and_arbitrary(self):
        v1: geom.Vector = geom.Vector(randp)
        v2: geom.Vector = geom.Vector(zerop)
        res = v1 ^ v2
        self.assertEqual(res, 0.0)

    def test_xor_parallel(self):
        v1: geom.Vector = geom.Vector(randp)
        v2: geom.Vector = geom.Vector(randp+randp, geom.Point(1.0, 1.0))
        res = v1 ^ v2
        self.assertEqual(res, 0.0)

    def test_xor_arbitrary(self):
        v1: geom.Vector = geom.Vector(geom.Point(rat_num*3, rat_num-12))
        v2: geom.Vector = geom.Vector(geom.Point(neg_num+4, rat_num))
        res = v1 ^ v2
        self.assertEqual(res, (rat_num*3)*(rat_num)-(rat_num-12)*(neg_num+4))


unittest.main()

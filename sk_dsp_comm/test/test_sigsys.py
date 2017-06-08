from unittest import TestCase

import numpy as np
from numpy.random import randn
from scipy import signal
import numpy.testing as npt
from sk_dsp_comm import sigsys as ss


class TestSigsys(TestCase):

    def test_cic_case_1(self):
        correct = np.ones(10) / 10
        b = ss.CIC(10,1)
        diff = correct - b
        diff = np.sum(diff)
        self.assertEqual(diff, 0)

    def test_cic_case_2(self):
        correct = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                   0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
        b = ss.CIC(10, 2)
        diff = correct - b
        diff = np.sum(diff)
        self.assertEqual(diff, 0)

    def test_ten_band_equalizer(self):
        w = randn(1000000)
        gdB = [x for x in range(1, 11)]
        y = ss.ten_band_eq_filt(w,gdB)
        yavg = np.average(y)
        npt.assert_almost_equal(abs(yavg), 0.001, decimal=2)

    def test_ten_band_equalizer_gdb_exception(self):
        w = randn(1000000)
        gdB = [x for x in range(1, 9)]
        with self.assertRaisesRegexp(ValueError, "GdB length not equal to ten") as ten_err:
            ss.ten_band_eq_filt(w,gdB)

    def test_peaking(self):
        b,a = ss.peaking(2.0, 500, 3.5, 44100)
        b_check = np.array([ 1.00458357, -1.95961252,  0.96001185])
        a_check = np.array([ 1.        , -1.95961252,  0.96459542])
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_ex6_2(self):
        n = np.arange(-5,8)
        x = ss.ex6_2(n)
        x_check = np.array([0., 0., 0., 10., 9., 8., 7., 6., 5., 4., 3.,
                            0., 0.])
        diff = x_check - x
        diff = np.sum(diff)
        self.assertEqual(diff, 0)

    def test_position_CD_fb_approx(self):
        Ka = 50
        b,a = ss.position_CD(Ka, 'fb_approx')
        b_check = np.array([ 254.64790895])
        a_check = np.array([   1.        ,   25.        ,  254.64790895])
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_position_CD_fb_exact(self):
        Ka = 50
        b, a = ss.position_CD(Ka, 'fb_exact')
        b_check = np.array([318309.88618379])
        a_check = np.array([1.00000000e+00, 1.27500000e+03, 3.12500000e+04,
                            3.18309886e+05])
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check, decimal=3)

    def test_position_CD_open_loop(self):
        Ka = 50
        b, a = ss.position_CD(Ka, 'open_loop')
        b_check = np.array([ 318309.88618379])
        a_check = np.array([    1,  1275, 31250,     0])
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_position_CD_out_type_value_error(self):
        Ka = 50
        with self.assertRaisesRegexp(ValueError, 'out_type must be: open_loop, fb_approx, or fc_exact') as cd_err:
            b, a = ss.position_CD(Ka, 'value_error')

    def test_cruise_control_H(self):
        wn = 0.1
        zeta = 1.0
        T = 10
        vcruise = 75
        vmax = 120
        b_check, a_check = (np.array([ 0.075,  0.01 ]), np.array([ 1.  ,  0.2 ,  0.01]))
        b,a = ss.cruise_control(wn, zeta, T, vcruise, vmax, tf_mode='H')
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_cruise_control_HE(self):
        wn = 0.1
        zeta = 1.0
        T = 10
        vcruise = 75
        vmax = 120
        b_check, a_check = (np.array([ 1.   ,  0.125,  0.   ]), np.array([ 1.  ,  0.2 ,  0.01]))
        b,a = ss.cruise_control(wn, zeta, T, vcruise, vmax, tf_mode='HE')
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_cruise_control_HVW(self):
        wn = 0.1
        zeta = 1.0
        T = 10
        vcruise = 75
        vmax = 120
        b_check, a_check = (np.array([ 0.00625   ,  0.00161458,  0.00010417]), np.array([ 1.  ,  0.2 ,  0.01]))
        b,a = ss.cruise_control(wn, zeta, T, vcruise, vmax, tf_mode='HVW')
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_cruise_control_HED(self):
        wn = 0.1
        zeta = 1.0
        T = 10
        vcruise = 75
        vmax = 120
        b_check, a_check = (np.array([ 20.04545455,   0.        ]), np.array([ 1.  ,  0.2 ,  0.01]))
        b,a = ss.cruise_control(wn, zeta, T, vcruise, vmax, tf_mode='HED')
        npt.assert_almost_equal(b, b_check)
        npt.assert_almost_equal(a, a_check)

    def test_cruise_control_tf_mode_value_error(self):
        wn = 0.1
        zeta = 1.0
        T = 10
        vcruise = 75
        vmax = 120
        with self.assertRaisesRegexp(ValueError, 'tf_mode must be: H, HE, HVU, or HED') as cc_err:
            b, a = ss.cruise_control(wn, zeta, T, vcruise, vmax, tf_mode='value_error')

    def test_prin_alias(self):
        f_in = np.arange(0,10,0.1)
        f_out_check = np.array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ,
        1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ,  2.1,
        2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3. ,  3.1,  3.2,
        3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4. ,  4.1,  4.2,  4.3,
        4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5. ,  4.9,  4.8,  4.7,  4.6,
        4.5,  4.4,  4.3,  4.2,  4.1,  4. ,  3.9,  3.8,  3.7,  3.6,  3.5,
        3.4,  3.3,  3.2,  3.1,  3. ,  2.9,  2.8,  2.7,  2.6,  2.5,  2.4,
        2.3,  2.2,  2.1,  2. ,  1.9,  1.8,  1.7,  1.6,  1.5,  1.4,  1.3,
        1.2,  1.1,  1. ,  0.9,  0.8,  0.7,  0.6,  0.5,  0.4,  0.3,  0.2,
        0.1])
        f_out = ss.prin_alias(f_in,10)
        npt.assert_almost_equal(f_out, f_out_check)

    def test_cascade_filters(self):
        b1,a1 = signal.butter(3,0.1)
        b2,a2 = signal.butter(3,0.15)
        b,a = ss.cascade_filters(b1,a1,b2,a2)
        b_check,a_check = (np.array([  2.49206659e-05,   1.49523995e-04,   3.73809988e-04,
         4.98413317e-04,   3.73809988e-04,   1.49523995e-04,
         2.49206659e-05]), np.array([ 1.        , -4.43923453,  8.35218582, -8.51113443,  4.94796745,
       -1.55360419,  0.20541481]))
        npt.assert_almost_equal(b,b_check)
        npt.assert_almost_equal(a,a_check)

    def test_fir_iir_notch_1(self):
        with self.assertRaisesRegexp(ValueError, 'Poles on or outside unit circle.') as nfi_err:
            b,a = ss.fir_iir_notch(1000,8000,1)

    def test_fir_iir_notch_0(self):
        b_FIR, a_FIR = ss.fir_iir_notch(1000, 8000, 0)
        b_FIR_check, a_FIR_check = (np.array([ 1.        , -1.41421356,  1.        ]), np.array([ 1.]))
        npt.assert_almost_equal(b_FIR, b_FIR_check)
        npt.assert_almost_equal(a_FIR, a_FIR_check)

    def test_fir_iir_notch_095(self):
        b_IIR, a_IIR = ss.fir_iir_notch(1000, 8000, r=0.95)
        b_IIR_check, a_IIR_check = (np.array([ 1.        , -1.41421356,  1.        ]),
                                    np.array([ 1.        , -1.34350288,  0.9025    ]))
        npt.assert_almost_equal(b_IIR, b_IIR_check)
        npt.assert_almost_equal(a_IIR, a_IIR_check)

    def test_fs_coeff_double_sided(self):
        t = np.arange(0, 1, 1/1024.)
        x_rect = ss.rect(t - .1, 0.2)
        Xk, fk = ss.fs_coeff(x_rect, 25, 10)
        Xk_check, fk_check = (np.array([  2.00195312e-01 +0.00000000e+00j,
         1.51763076e-01 -1.09694238e-01j,
         4.74997396e-02 -1.43783764e-01j,
        -3.04576408e-02 -9.61419900e-02j,
        -3.74435130e-02 -2.77700018e-02j,
         1.95305146e-04 +2.39687506e-06j,
         2.56251893e-02 -1.80472945e-02j,
         1.40893600e-02 -4.09547511e-02j,
        -1.09682089e-02 -3.61573392e-02j,
        -1.64204592e-02 -1.24934761e-02j,
         1.95283084e-04 +4.79393062e-06j,
         1.41580149e-02 -9.71348931e-03j,
         8.52093529e-03 -2.38144188e-02j,
        -6.47058053e-03 -2.23127601e-02j,
        -1.04138132e-02 -8.12701956e-03j,
         1.95246305e-04 +7.19134726e-06j,
         9.85775554e-03 -6.58674167e-03j,
         6.22804508e-03 -1.67550994e-02j,
        -4.47157604e-03 -1.61581996e-02j,
        -7.56851964e-03 -6.05743025e-03j,
         1.95194801e-04 +9.58930569e-06j,
         7.60518287e-03 -4.94771418e-03j,
         4.97737845e-03 -1.29033684e-02j,
        -3.34165027e-03 -1.26784330e-02j,
        -5.90873600e-03 -4.84917431e-03j,   1.95128558e-04 +1.19879869e-05j]), np.array([  0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100, 110, 120,
       130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]))
        npt.assert_almost_equal(Xk, Xk_check)
        npt.assert_almost_equal(fk, fk_check)

    def test_fs_coeff_single_sided(self):
        t = np.arange(0,1,1/1024.)
        x_rect = ss.rect(t-.1,0.2)
        Xk, fk = ss.fs_coeff(x_rect, 25, 10, one_side=False)
        Xk_check, fk_check = (np.array([  1.95128558e-04 -1.19879869e-05j,
        -5.90873600e-03 +4.84917431e-03j,
        -3.34165027e-03 +1.26784330e-02j,
         4.97737845e-03 +1.29033684e-02j,
         7.60518287e-03 +4.94771418e-03j,
         1.95194801e-04 -9.58930569e-06j,
        -7.56851964e-03 +6.05743025e-03j,
        -4.47157604e-03 +1.61581996e-02j,
         6.22804508e-03 +1.67550994e-02j,
         9.85775554e-03 +6.58674167e-03j,
         1.95246305e-04 -7.19134726e-06j,
        -1.04138132e-02 +8.12701956e-03j,
        -6.47058053e-03 +2.23127601e-02j,
         8.52093529e-03 +2.38144188e-02j,
         1.41580149e-02 +9.71348931e-03j,
         1.95283084e-04 -4.79393062e-06j,
        -1.64204592e-02 +1.24934761e-02j,
        -1.09682089e-02 +3.61573392e-02j,
         1.40893600e-02 +4.09547511e-02j,
         2.56251893e-02 +1.80472945e-02j,
         1.95305146e-04 -2.39687506e-06j,
        -3.74435130e-02 +2.77700018e-02j,
        -3.04576408e-02 +9.61419900e-02j,
         4.74997396e-02 +1.43783764e-01j,
         1.51763076e-01 +1.09694238e-01j,
         2.00195312e-01 +0.00000000e+00j,
         1.51763076e-01 -1.09694238e-01j,
         4.74997396e-02 -1.43783764e-01j,
        -3.04576408e-02 -9.61419900e-02j,
        -3.74435130e-02 -2.77700018e-02j,
         1.95305146e-04 +2.39687506e-06j,
         2.56251893e-02 -1.80472945e-02j,
         1.40893600e-02 -4.09547511e-02j,
        -1.09682089e-02 -3.61573392e-02j,
        -1.64204592e-02 -1.24934761e-02j,
         1.95283084e-04 +4.79393062e-06j,
         1.41580149e-02 -9.71348931e-03j,
         8.52093529e-03 -2.38144188e-02j,
        -6.47058053e-03 -2.23127601e-02j,
        -1.04138132e-02 -8.12701956e-03j,
         1.95246305e-04 +7.19134726e-06j,
         9.85775554e-03 -6.58674167e-03j,
         6.22804508e-03 -1.67550994e-02j,
        -4.47157604e-03 -1.61581996e-02j,
        -7.56851964e-03 -6.05743025e-03j,
         1.95194801e-04 +9.58930569e-06j,
         7.60518287e-03 -4.94771418e-03j,
         4.97737845e-03 -1.29033684e-02j,
        -3.34165027e-03 -1.26784330e-02j,
        -5.90873600e-03 -4.84917431e-03j,   1.95128558e-04 +1.19879869e-05j]), np.array([-250, -240, -230, -220, -210, -200, -190, -180, -170, -160, -150,
       -140, -130, -120, -110, -100,  -90,  -80,  -70,  -60,  -50,  -40,
        -30,  -20,  -10,    0,   10,   20,   30,   40,   50,   60,   70,
         80,   90,  100,  110,  120,  130,  140,  150,  160,  170,  180,
        190,  200,  210,  220,  230,  240,  250]))
        npt.assert_almost_equal(Xk, Xk_check)
        npt.assert_almost_equal(fk, fk_check)

    def test_fs_coeff_value_error(self):
        t = np.arange(0,1,1/1024.)
        x_rect = ss.rect(t-.1, 0.2)
        with self.assertRaisesRegexp(ValueError, 'Number of samples in xp insufficient for requested N.') as fsc_err:
            Xk, fk = ss.fs_coeff(x_rect, 2**13, 10)
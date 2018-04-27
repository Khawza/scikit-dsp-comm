from unittest import TestCase
from sk_dsp_comm import fec_conv
from .test_helper import SKDSPCommTest
import numpy as np
from numpy import testing as npt
from sk_dsp_comm import digitalcom as dc

class TestFecConv(SKDSPCommTest):
    _multiprocess_can_split_ = True

    def test_fec_conv_inst(self):
        cc1 = fec_conv.fec_conv(('101', '111'), Depth=10)  # decision depth is 10

    def test_fec_conv_conv_encoder(self):
        cc1 = fec_conv.fec_conv()
        x = np.random.randint(0, 2, 20)
        state = '00'
        y_test, state_test = (np.array([ 0.,  0.,  0.,  0.,  1.,  1.,  0.,  1.,  1.,  0.,  1.,  0.,  0.,
        1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,
        1.,  1.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  1.,  1.,  1.,  1.]), '10')
        y, state = cc1.conv_encoder(x, state)
        npt.assert_almost_equal(y_test, y)
        self.assertEqual(state_test, state)

    def test_fec_conv_viterbi_decoder(self):
        cc1 = fec_conv.fec_conv()
        x = np.random.randint(0,2,20)
        state = '00'
        y, state = cc1.conv_encoder(x, state)
        z_test = [ 0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.]
        yn = dc.cpx_AWGN(2 * y - 1, 5, 1)
        yn = (yn.real + 1) / 2 * 7
        z = cc1.viterbi_decoder(yn)
        npt.assert_almost_equal(z_test, z)
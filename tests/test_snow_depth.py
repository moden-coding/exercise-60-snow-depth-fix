#!/usr/bin/env python3

import contextlib
import io
import os
import unittest
from unittest.mock import patch

import pandas as pd

from src.snow_depth import main, snow_depth


class SnowDepth(unittest.TestCase):

    def test_value(self):
        ret_val = snow_depth()
        self.assertEqual(ret_val, 15.0, msg="Incorrect return value!")

    def test_output(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        out = buf.getvalue().strip()
        pattern = r"Max snow depth:\s+\d+.\d"
        self.assertRegex(out, pattern, msg="Output is not in correct form!")

    def test_called(self):
        with patch(
            "src.snow_depth.snow_depth", wraps=snow_depth
        ) as psd, patch(
            "src.snow_depth.pd.read_csv", wraps=pd.read_csv
        ) as prc:
            main()
            psd.assert_called_once()
            prc.assert_called_once()
            args, kwargs = prc.call_args
            self.assertEqual(
                os.path.basename(args[0]),
                "kumpula-weather-2017.csv",
                msg="Wrong filename was given to read_csv!",
            )
            if "sep" in kwargs:
                self.assertEqual(
                    kwargs["sep"],
                    ",",
                    msg="Incorrect separator in call to read_csv!",
                )


if __name__ == "__main__":
    unittest.main()

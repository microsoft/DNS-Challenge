import argparse
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import resampy
import soundfile as sf
import torch
import torchaudio
import torchvision

import audiolib
from DNSMOS.dnsmos_local import ComputeScore
import noisyspeech_synthesizer_singleprocess as synthesizer
import pdns_noisyspeech_synthesizer_singleprocess as personalized_synthesizer


ROOT = Path(__file__).resolve().parent


class DependencySmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.directory = Path(self.temp_dir.name)
        self.sample_rate = 16000
        time = np.arange(self.sample_rate) / self.sample_rate
        self.audio = 0.1 * np.sin(2 * np.pi * 440 * time)

    def test_pytorch_companion_operations(self):
        waveform = torch.from_numpy(self.audio).float().unsqueeze(0)
        resampled = torchaudio.transforms.Resample(16000, 8000)(waveform)
        self.assertEqual(tuple(resampled.shape), (1, 8000))
        self.assertTrue(torch.isfinite(resampled).all())
        boxes = torch.tensor([[0, 0, 10, 10], [1, 1, 9, 9]], dtype=torch.float32)
        kept = torchvision.ops.nms(boxes, torch.tensor([0.9, 0.8]), 0.5)
        self.assertEqual(kept.tolist(), [0])

    def test_audio_io_normalization_and_mixing(self):
        path = self.directory / "audio.wav"
        audiolib.audiowrite(str(path), self.audio, self.sample_rate)
        audio, sample_rate = audiolib.audioread(str(path))
        self.assertEqual(sample_rate, self.sample_rate)
        np.testing.assert_allclose(audio, self.audio, atol=1 / 32768)
        normalized = audiolib.normalize(audio)
        self.assertAlmostEqual(20 * np.log10(np.sqrt(np.mean(normalized ** 2))), -25)
        noise = np.random.default_rng(0).normal(0, 0.1, len(audio))
        params = {"cfg": {}, "target_level_lower": -30, "target_level_upper": -20}
        clean, noise, mixture, _ = audiolib.snr_mixer(
            params, audio, noise, 10
        )
        np.testing.assert_allclose(mixture, clean + noise, atol=1e-12)
        snr = 10 * np.log10(np.mean(clean ** 2) / np.mean(noise ** 2))
        self.assertAlmostEqual(snr, 10, places=6)
        self.assertFalse(audiolib.is_clipped(mixture))
        clean, noise, mixture, _ = audiolib.segmental_snr_mixer(
            params, audio, noise, 10
        )
        np.testing.assert_allclose(mixture, clean + noise, atol=1e-12)
        self.assertTrue(np.isfinite(mixture).all())

    def test_synthesizers_resample_input(self):
        path = self.directory / "input.wav"
        sf.write(path, self.audio, self.sample_rate)
        params = {
            "fs": 8000,
            "silence_length": 0.1,
            "audio_length": 1,
            "cleanfilenames": [str(path)],
            "is_test_set": True,
        }
        expected = resampy.resample(sf.read(path)[0], self.sample_rate, params["fs"])
        for module in (synthesizer, personalized_synthesizer):
            with self.subTest(synthesizer=module.__name__):
                audio, files, clipped, _ = module.build_audio(True, params, 0)
                self.assertEqual(files, [str(path)])
                self.assertEqual(clipped, [])
                np.testing.assert_allclose(audio, expected)

    def test_audio_directory_resampling(self):
        path = self.directory / "input.wav"
        sf.write(path, self.audio, self.sample_rate)
        expected = resampy.resample(sf.read(path)[0], self.sample_rate, 8000)
        with contextlib.redirect_stdout(io.StringIO()):
            audiolib.resampler(str(self.directory), target_sr=8000)
        audio, sample_rate = sf.read(path)
        self.assertEqual(sample_rate, 8000)
        np.testing.assert_allclose(audio, expected, atol=1 / 32768)

    def test_dnsmos_models_and_resampling(self):
        # Captured with librosa 0.8.1, before the dependency upgrade.
        baseline = {
            (False, 16000): (1.2787537, 1.1505890, 1.0289310, 2.4171488),
            (False, 8000): (1.2787216, 1.1506490, 1.0289162, 2.4424675),
            (True, 16000): (2.4305229, 2.0414963, 1.7665725, 2.4171488),
            (True, 8000): (2.4290514, 2.0377491, 1.7656795, 2.4424675),
        }
        for personalized in (False, True):
            model_dir = "pDNSMOS" if personalized else "DNSMOS"
            scorer = ComputeScore(
                str(ROOT / "DNSMOS" / model_dir / "sig_bak_ovr.onnx"),
                str(ROOT / "DNSMOS" / "DNSMOS" / "model_v8.onnx"),
            )
            for sample_rate in (16000, 8000):
                with self.subTest(personalized=personalized, sample_rate=sample_rate):
                    audio = np.tile(self.audio[::16000 // sample_rate], 10)
                    path = self.directory / f"audio-{sample_rate}.wav"
                    sf.write(path, audio, sample_rate)
                    result = scorer(str(path), 16000, personalized)
                    self.assertEqual(result["sr"], 16000)
                    self.assertAlmostEqual(result["len_in_sec"], 10)
                    self.assertEqual(result["num_hops"], 1)
                    for metric in ("SIG", "BAK", "OVRL", "P808_MOS"):
                        self.assertTrue(np.isfinite(result[metric]), metric)
                    np.testing.assert_allclose(
                        [result[key] for key in ("SIG", "BAK", "OVRL", "P808_MOS")],
                        baseline[(personalized, sample_rate)],
                        rtol=0,
                        atol=1e-4,
                    )

    def test_wacc_resampling_and_csv_with_mock_service(self):
        spec = importlib.util.spec_from_file_location("wacc", ROOT / "WAcc" / "WAcc.py")
        wacc = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, {"WACC_SERVICE_URL": "https://example.invalid/score"}):
            spec.loader.exec_module(wacc)
        path = self.directory / "input.wav"
        sf.write(path, self.audio[::2], 8000)
        original_audio, original_rate = sf.read(path)
        transcriptions = self.directory / "transcriptions.tsv"
        pd.DataFrame({"filename": [path.name]}).to_csv(
            transcriptions, sep="\t", index=False
        )
        output = self.directory / "scores.csv"

        def score_audio(url, files):
            self.assertEqual(url, "https://example.invalid/score")
            audio, rate = sf.read(files["audiodata"])
            self.assertEqual(rate, 16000)
            self.assertEqual(len(audio), 16000)
            response = unittest.mock.Mock()
            response.json.return_value = 0.9
            return response

        args = argparse.Namespace(testset_dir=str(self.directory), score_file=str(output))
        with patch.object(wacc, "TRANSCRIPTIONS_FILE", str(transcriptions)), \
                patch.object(wacc.requests, "post", side_effect=score_audio) as post, \
                contextlib.redirect_stdout(io.StringIO()):
            wacc.main(args)
        post.assert_called_once()
        self.assertEqual(pd.read_csv(output)["wacc"].tolist(), [0.9])
        restored_audio, restored_rate = sf.read(path)
        self.assertEqual(restored_rate, original_rate)
        np.testing.assert_array_equal(restored_audio, original_audio)

    def test_wacc_requires_explicit_service_configuration(self):
        spec = importlib.util.spec_from_file_location("wacc", ROOT / "WAcc" / "WAcc.py")
        wacc = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, {"WACC_SERVICE_URL": ""}):
            spec.loader.exec_module(wacc)
        with patch.object(wacc.requests, "post") as post:
            with self.assertRaisesRegex(ValueError, "Set WACC_SERVICE_URL"):
                wacc.main(argparse.Namespace(testset_dir=str(self.directory), score_file=None))
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()

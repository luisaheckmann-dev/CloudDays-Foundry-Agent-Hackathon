import contextlib
import io
import os
import unittest
from unittest.mock import patch

from orderops.__main__ import main
from orderops.config import Settings, check_packages
from orderops.evaluation import dataset, structural_checks
from orderops.runtime import RunResult
from orderops.tools import Dispatcher


class ConfigTests(unittest.TestCase):
    def test_sdk_pins_installed(self):
        self.assertEqual(check_packages()["azure-ai-projects"], "2.10.0")

    def test_cloud_opt_in_is_required_for_every_cloud_command(self):
        for command in ("preflight", "upload", "register", "chat", "smoke", "evaluate", "cleanup"):
            args = [command] + (["--confirm", "anything"] if command == "cleanup" else [])
            with self.subTest(command=command), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(args), 1)

    def test_mutually_exclusive_modes(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["preflight", "--offline", "--allow-cloud"]), 1)

    @patch("orderops.config.load_env")
    def test_valid_config_and_bad_endpoints(self, _):
        base = {"FOUNDRY_PROJECT_ENDPOINT": "https://demo.services.ai.azure.com/api/projects/lab",
                "FOUNDRY_MODEL_DEPLOYMENT_NAME": "team-deployment", "FOUNDRY_AGENT_NAME": "team-01"}
        with patch.dict(os.environ, base, clear=True):
            self.assertEqual(Settings.read().agent, "team-01")
            for endpoint in ("", "http://demo.services.ai.azure.com/api/projects/lab",
                             "https://evil.example/api/projects/lab",
                             "https://demo.services.ai.azure.com/",
                             "https://demo.services.ai.azure.com/api/projects/lab?secret=x"):
                with self.subTest(endpoint=endpoint), patch.dict(os.environ, {"FOUNDRY_PROJECT_ENDPOINT": endpoint}):
                    with self.assertRaises(ValueError):
                        Settings.read()
        with patch.dict(os.environ, {**base, "FOUNDRY_AGENT_NAME": "orderops-YOUR-TEAM"}, clear=True):
            with self.assertRaises(ValueError):
                Settings.read()
        with patch.dict(os.environ, {**base, "AZURE_SUBSCRIPTION_ID":
                                    "11111111-2222-3333-4444-555555555555"}, clear=True):
            self.assertEqual(Settings.read().subscription, "11111111-2222-3333-4444-555555555555")
            with patch.dict(os.environ, {"AZURE_SUBSCRIPTION_ID": "not-a-subscription"}):
                with self.assertRaises(ValueError):
                    Settings.read()
        with self.assertRaises(ValueError):
            Settings(base["FOUNDRY_PROJECT_ENDPOINT"], "model", "agent",
                     tenant="22222222-2222-2222-2222-222222222222",
                     subscription="11111111-2222-3333-4444-555555555555")

    def test_required_evaluation_cases(self):
        cases = {case["id"] for case in dataset()}
        self.assertTrue({"normal", "unsupported", "nonexistent", "insufficient", "policy-conflict",
                         "injection", "denied-approval", "duplicate", "desired-citation"} <= cases)
        self.assertEqual(len(cases), len(dataset()))

    def test_fake_citations_and_plain_filename_do_not_pass(self):
        case = next(case for case in dataset() if case["id"] == "desired-citation")
        result = RunResult("20: order-policy-2026-11.txt", citations=[])
        checks = structural_checks(case, result, Dispatcher(), ["file-real"])
        self.assertFalse(checks["citation_present_and_known"])
        self.assertFalse(checks["current_filename_annotation"])
        result.citations = [{"file_id": "file-invented", "filename": "order-policy-2026-11.txt"}]
        self.assertFalse(structural_checks(case, result, Dispatcher(),
                                          ["file-real"])["citation_present_and_known"])

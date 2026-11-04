import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from orderops import cloud, state
from orderops.config import Settings


class CloudContractTests(unittest.TestCase):
    """Mocked contracts, never network and never evidence of a cloud pass."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="orderops-unittest-")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.settings = Settings("https://unit.services.ai.azure.com/api/projects/unit",
                                 "deployment-unit", "agent-unit")
        self.api = Mock()
        self.project = Mock()
        self.credential = Mock()
        for target, value in (("orderops.state.LOCAL", self.work),
                              ("orderops.cloud.Settings.read", self.settings)):
            patcher = patch(target, return_value=value) if target.endswith(".read") else patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)

        @contextlib.contextmanager
        def fake_clients(_):
            yield self.credential, self.project, self.api
        patcher = patch("orderops.cloud.clients", fake_clients)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.out = contextlib.redirect_stdout(io.StringIO())
        self.out.__enter__()
        self.addCleanup(self.out.__exit__, None, None, None)

    def test_upload_tracks_owned_resources_and_waits_for_completed(self):
        self.api.vector_stores.create.return_value = NS(id="vs-unit")
        self.api.files.create.side_effect = [NS(id="file-a"), NS(id="file-b")]
        self.api.vector_stores.files.retrieve.return_value = NS(status="completed")
        cloud.upload()
        manifest = state.read_state(self.settings)
        self.assertEqual(manifest["active_vector_store"], "vs-unit")
        self.assertEqual(manifest["file_ids"], ["file-a", "file-b"])
        self.assertEqual(self.api.vector_stores.files.retrieve.call_count, 2)
        self.assertEqual(self.api.files.create.call_args.kwargs["purpose"], "assistants")

    def test_failed_ingestion_never_marks_store_ready_and_preserves_manifest(self):
        self.api.vector_stores.create.return_value = NS(id="vs-unit")
        self.api.files.create.return_value = NS(id="file-a")
        self.api.vector_stores.files.retrieve.return_value = NS(status="failed")
        with self.assertRaises(RuntimeError):
            cloud.upload()
        manifest = state.read_state(self.settings)
        self.assertIsNone(manifest["active_vector_store"])
        self.assertEqual(manifest["vector_store_ids"], ["vs-unit"])
        self.assertEqual(manifest["file_ids"], ["file-a"])

    def test_register_records_version_and_track(self):
        manifest = state.read_state(self.settings, create=True)
        manifest["active_vector_store"] = "vs-unit"
        state.save_state(manifest)
        self.project.agents.create_version.return_value = NS(name="agent-unit", version="9")
        cloud.register("solution")
        current = state.read_state(self.settings)["active_agent"]
        self.assertEqual(current, {"name": "agent-unit", "version": "9", "track": "solution"})
        definition = self.project.agents.create_version.call_args.kwargs["definition"].as_dict()
        self.assertEqual(definition["model"], "deployment-unit")
        self.assertEqual(definition["tools"][0]["type"], "file_search")
        self.assertEqual(definition["tools"][0]["vector_store_ids"], ["vs-unit"])

    def test_manifest_cross_project_blocked(self):
        state.save_state(state.read_state(self.settings, create=True))
        with self.assertRaises(ValueError):
            state.read_state(Settings("https://other.services.ai.azure.com/api/projects/other",
                                      "model", "agent-unit"))

    def test_cleanup_exact_confirmation_and_no_broad_delete(self):
        manifest = state.read_state(self.settings, create=True)
        manifest.update(file_ids=["file-unit"], vector_store_ids=["vs-unit"],
                        response_ids=["resp-unit"],
                        versions=[{"name": "agent-unit", "version": "9", "track": "solution"}])
        state.save_state(manifest)
        with self.assertRaises(ValueError):
            cloud.cleanup("not-the-agent")
        self.project.agents.delete_version.assert_not_called()
        cloud.cleanup("agent-unit")
        self.project.agents.delete_version.assert_called_once_with(agent_name="agent-unit", agent_version="9")
        self.api.files.delete.assert_called_once_with("file-unit")
        self.api.responses.delete.assert_called_once_with("resp-unit")
        self.api.vector_stores.delete.assert_called_once_with("vs-unit")
        self.project.agents.delete.assert_not_called()
        self.assertEqual(state.read_state(self.settings)["file_ids"], [])

    def test_cleanup_failure_retains_owned_id_for_retry(self):
        manifest = state.read_state(self.settings, create=True)
        manifest["file_ids"] = ["file-unit"]
        state.save_state(manifest)
        self.api.files.delete.side_effect = ConnectionError("mock only")
        with self.assertRaises(RuntimeError):
            cloud.cleanup("agent-unit")
        self.assertEqual(state.read_state(self.settings)["file_ids"], ["file-unit"])

    def test_preflight_has_no_model_fallback(self):
        self.project.deployments.list.return_value = [NS(name="different-deployment")]
        with self.assertRaises(ValueError):
            cloud.preflight()
        self.api.responses.create.assert_not_called()

    def test_diagnostics_do_not_store_prompt_or_response_text(self):
        state.diagnostic("response", response_id="resp-unit", tokens=30)
        record = json.loads((self.work / "diagnostics.jsonl").read_text(encoding="utf-8"))
        self.assertNotIn("prompt", record)
        self.assertNotIn("response", record)
        self.assertEqual(record["response_id"], "resp-unit")

    def test_state_retries_only_transient_windows_permission_errors(self):
        locked = PermissionError("temporary Windows file lock")
        locked.winerror = 32
        with patch.object(Path, "replace", side_effect=[locked, None]) as replace:
            with patch("orderops.state.time.sleep") as sleep:
                state.save_state(state.read_state(self.settings, create=True))
        self.assertEqual(replace.call_count, 2)
        sleep.assert_called_once_with(0.05)

    def test_state_does_not_hide_persistent_permission_errors(self):
        with patch.object(Path, "replace", side_effect=PermissionError("access denied")):
            with patch("orderops.state.time.sleep") as sleep:
                with self.assertRaises(PermissionError):
                    state.save_state(state.read_state(self.settings, create=True))
        sleep.assert_not_called()

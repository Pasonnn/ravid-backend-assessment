from __future__ import annotations

import json
from pathlib import Path

from django.test import SimpleTestCase


class ObservabilityDashboardUnitTests(SimpleTestCase):
    def test_service_variable_uses_non_empty_compatible_all_value(self) -> None:
        dashboard = self._load_dashboard()
        service_var = next(
            item
            for item in dashboard["templating"]["list"]
            if item["name"] == "service"
        )
        self.assertEqual(service_var["allValue"], "django|celery")
        self.assertEqual(service_var["current"]["value"], "django|celery")
        self.assertIn("django|celery", service_var["query"])

    def test_dashboard_queries_do_not_use_empty_compatible_service_regex(self) -> None:
        dashboard = self._load_dashboard()

        expressions: list[str] = []
        for panel in dashboard["panels"]:
            for target in panel.get("targets", []):
                expr = target.get("expr")
                if isinstance(expr, str):
                    expressions.append(expr)

        self.assertTrue(expressions)
        self.assertFalse(any('service=~".*"' in expr for expr in expressions))

    def _load_dashboard(self) -> dict[str, object]:
        dashboard_path = Path("docker/grafana/dashboards/observability-overview.json")
        return json.loads(dashboard_path.read_text(encoding="utf-8"))

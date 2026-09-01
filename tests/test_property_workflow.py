import unittest

from src.property_workflow import decide_priority


class MaintenanceRoutingTest(unittest.TestCase):
    def test_water_leak_is_sent_to_urgent_queue(self) -> None:
        result = decide_priority("Water is leaking under the kitchen sink.")
        self.assertEqual(result, "urgent")

    def test_paint_touch_up_stays_routine(self) -> None:
        result = decide_priority("Please touch up the bedroom paint.")
        self.assertEqual(result, "routine")


if __name__ == "__main__":
    unittest.main()


import unittest

from listen_inventory import format_listeners, parse_proc_net_tcp

SAMPLE_TCP = """  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0100007F:1F90 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12345 1 0000000000000000 100 0 0 10 0
   1: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12346 1 0000000000000000 100 0 0 10 0
   2: 0100007F:0050 0100007F:C351 01 00000000:00000000 00:00000000 00000000     0        0 12347 1 0000000000000000 100 0 0 10 0
"""


class ListenInventoryTests(unittest.TestCase):
    def test_parses_listen_rows_only(self):
        rows = parse_proc_net_tcp(SAMPLE_TCP)
        self.assertEqual(rows, [("127.0.0.1", 8080), ("0.0.0.0", 22)])

    def test_empty_text(self):
        self.assertEqual(parse_proc_net_tcp(""), [])

    def test_format_empty(self):
        text = format_listeners([])
        self.assertIn("No TCP listeners", text)


if __name__ == "__main__":
    unittest.main()

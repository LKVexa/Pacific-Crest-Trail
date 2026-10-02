"""Cancelled client requests must not become a second storage-error response."""
import io
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from server import Handler


class ResponseDisconnectTests(unittest.TestCase):
    def response(self, command='GET', header_error=None, body_error=None):
        handler = object.__new__(Handler)
        handler.command = command
        handler.close_connection = False
        statuses = []
        handler.send_response = statuses.append
        handler.send_header = lambda *args: None
        def end_headers():
            if header_error:
                raise header_error('viewer disconnected during headers')
        handler.end_headers = end_headers
        class Writer(io.BytesIO):
            def write(self, value):
                if body_error:
                    raise body_error('viewer cancelled an image')
                return super().write(value)
        handler.wfile = Writer()
        return handler, statuses

    def test_cancelled_headers_and_body_close_once(self):
        for error in (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            for location in ('header_error', 'body_error'):
                with self.subTest(error=error.__name__, location=location):
                    handler, statuses = self.response(**{location: error})
                    handler.send_payload(200, b'original image')
                    self.assertTrue(handler.close_connection)
                    self.assertEqual(statuses, [200])

    def test_successful_get_retains_bytes(self):
        handler, statuses = self.response()
        handler.send_payload(200, b'original image')
        self.assertEqual(handler.wfile.getvalue(), b'original image')
        self.assertEqual(statuses, [200])
        self.assertFalse(handler.close_connection)

    def test_head_sends_no_body(self):
        handler, statuses = self.response(command='HEAD', body_error=ConnectionAbortedError)
        handler.send_payload(200, b'original image')
        self.assertEqual(handler.wfile.getvalue(), b'')
        self.assertEqual(statuses, [200])
        self.assertFalse(handler.close_connection)


if __name__ == '__main__':
    unittest.main()

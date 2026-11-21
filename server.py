
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import path
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
import json
from email_sender import send_customer_report
BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"


class SalesCRMHandler(BaseHTTPRequestHandler):

    def send_content(self, content, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):

        path = urlparse(self.path).path

        # 1. Display HTML page
        if path == "/":
            html_file = BASE_DIR / "templates" / "index.html"

            self.send_content(
                html_file.read_bytes(),
                "text/html; charset=utf-8"
            )

        # 2. Display CSS
        elif path == "/static/style.css":
            css_file = BASE_DIR / "static" / "style.css"

            self.send_content(
                css_file.read_bytes(),
                "text/css; charset=utf-8"
            )

        # 3. Send customer report information as JSON
        elif path == "/api/reports":

            customers = []

            for file in REPORTS_DIR.glob("*.xlsx"):

                try:
                    df = pd.read_excel(
                        file,
                        sheet_name="Order Details"
                    )

                    if df.empty:
                        continue

                    customer = {
                        "customer_id": int(df["customer_id"].iloc[0]),
                        "customer_name": str(df["customer_name"].iloc[0]),
                        "email": str(df["email"].iloc[0]),
                        "total_orders": int(df["order_id"].nunique()),
                        "total_sales": float(df["total_amount"].sum()),
                        "report_file": file.name
                    }

                    customers.append(customer)

                except Exception as error:
                    print(f"Could not read {file.name}: {error}")

            response = json.dumps(customers).encode("utf-8")

            self.send_content(
                response,
                "application/json; charset=utf-8"
            )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")

    def do_POST(self):

        path = urlparse(self.path).path

        if path == "/api/send-report":

         content_length = int(
            self.headers.get("Content-Length", 0)
        )

        if content_length <= 0 or content_length > 4096:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "success": False,
                    "message": "Invalid request."
                }).encode("utf-8")
            )
            return

        try:
            post_data = self.rfile.read(content_length)

            data = json.loads(post_data.decode("utf-8"))

            customer_id = data.get("customer_id")

            if (
                isinstance(customer_id, bool)
                or not isinstance(customer_id, int)
                or customer_id <= 0
            ):
                raise ValueError("Invalid customer ID.")

            # Call the email function
            result = send_customer_report(customer_id)

            response = json.dumps(result).encode("utf-8")

            self.send_response(
                200 if result["success"] else 400
            )

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )

            self.end_headers()
            self.wfile.write(response)

        except (
            ValueError,
            UnicodeDecodeError,
            json.JSONDecodeError
        ) as error:

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "message": str(error)
                }).encode("utf-8")
            )

    # else:
    #     self.send_response(404)
    #     self.end_headers()


server = ThreadingHTTPServer(
    ("127.0.0.1", 8000),
    SalesCRMHandler
)

print("Sales CRM server running at http://127.0.0.1:8000")

server.serve_forever()

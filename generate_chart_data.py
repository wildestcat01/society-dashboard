from datetime import datetime

def generate_payment_chart_data(payments):
    chart_labels = []
    chart_data = []
    chart_delays = []

    for payment in payments:
        month_label = payment.get("month_paid_for")
        paid_on_str = payment.get("created_at")

        chart_labels.append(month_label)
        chart_data.append(payment.get("amount", 0))

        # Calculate delay in days
        try:
            due_date = datetime.strptime(f"{month_label}-01", "%Y-%m-%d")
            paid_date = datetime.fromisoformat(paid_on_str.replace("Z", "+00:00"))
            delay = (paid_date - due_date).days
        except Exception:
            delay = 0

        chart_delays.append(max(delay, 0))

    return chart_labels, chart_data, chart_delays

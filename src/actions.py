from datetime import date, timedelta
import uuid

def seed_actions():
    return [{"id": "T9-1042", "title": "Review Beta supplier renegotiation", "brand": "Brand Beta", "owner": "Operations Team", "priority": "High", "status": "In Progress", "due": "2026-03-04"}, {"id": "T9-1038", "title": "Document Alpha 250 ml pilot results", "brand": "Brand Alpha", "owner": "Product Team", "priority": "Medium", "status": "Open", "due": "2026-03-08"}, {"id": "T9-1029", "title": "Refresh UGC creative playbook", "brand": "Brand Gamma", "owner": "Growth Team", "priority": "Low", "status": "Completed", "due": "2026-02-20"}]

def create_action(form):
    return {"id": f"T9-{uuid.uuid4().hex[:6].upper()}", "title": form["title"], "brand": form["brand"], "owner": form["owner"], "priority": form["priority"], "status": "Open", "due": str(form.get("deadline") or date.today() + timedelta(days=30)), "description": form.get("description", "")}

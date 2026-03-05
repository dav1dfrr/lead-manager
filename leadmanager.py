#!/usr/bin/env python3
"""Lead Management System - Portfolio Piece"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).parent / "leads.json"

STATUSES = {
    "new": {"label": "🆕 New"},
    "contacted": {"label": "📞 Contacted"},
    "qualified": {"label": "✅ Qualified"},
    "proposal": {"label": "📄 Proposal"},
    "won": {"label": "💰 Won"},
    "lost": {"label": "❌ Lost"},
}

def load_leads():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_leads(leads):
    with open(DATA_FILE, "w") as f:
        json.dump(leads, f, indent=2)

def get_next_id(leads):
    if not leads:
        return 1
    return max(l["id"] for l in leads) + 1

def add_lead(company, contact, email, description, value):
    leads = load_leads()
    lead = {
        "id": get_next_id(leads),
        "company": company,
        "contact": contact,
        "email": email,
        "description": description,
        "value": float(value),
        "status": "new",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "follow_up": (datetime.now() + timedelta(days=3)).isoformat(),
    }
    leads.append(lead)
    save_leads(leads)
    print(f"✓ Added lead: {company}")
    return lead

def list_leads():
    leads = load_leads()
    if not leads:
        print("No leads yet. Add one with: python lead_manager.py add ...")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<4} {'COMPANY':<20} {'CONTACT':<15} {'STATUS':<15} {'VALUE':<10}")
    print("="*80)
    
    total_value = 0
    for lead in leads:
        status_info = STATUSES.get(lead["status"], STATUSES["new"])
        print(f"{lead['id']:<4} {lead['company'][:19]:<20} {lead['contact'][:14]:<15} {status_info['label']:<15} ${lead['value']:,.0f}")
        total_value += lead["value"]
    
    print("="*80)
    print(f"Total Pipeline Value: ${total_value:,.0f}")
    print(f"Total Leads: {len(leads)}")

def update_lead(lead_id, status=None, value=None):
    leads = load_leads()
    for lead in leads:
        if lead["id"] == int(lead_id):
            if status:
                if status not in STATUSES:
                    print(f"Invalid status. Options: {', '.join(STATUSES.keys())}")
                    return
                lead["status"] = status
            if value:
                lead["value"] = float(value)
            lead["updated"] = datetime.now().isoformat()
            save_leads(leads)
            print(f"✓ Updated lead {lead_id}")
            return
    print(f"Lead {lead_id} not found")

def show_dashboard():
    leads = load_leads()
    if not leads:
        print("No data. Add leads first!")
        return
    
    won_value = sum(l["value"] for l in leads if l["status"] == "won")
    pipeline_value = sum(l["value"] for l in leads if l["status"] != "lost")
    
    print(f"\n💰 TOTAL WON: ${won_value:,.0f}")
    print(f"📊 PIPELINE:  ${pipeline_value:,.0f}")
    print(f"👥 TOTAL LEADS: {len(leads)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python lead_manager.py <init|add|list|update|dashboard>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        save_leads([])
        print("✓ Initialized")
    elif cmd == "add":
        if len(sys.argv) < 7:
            print('Usage: add "Company" "Contact" email@.com "desc" value')
            return
        _, _, company, contact, email, description, value = sys.argv[:7]
        add_lead(company, contact, email, description, value)
    elif cmd == "list":
        list_leads()
    elif cmd == "update":
lead_id = sys.argv[2]
        status = sys.argv[4] if len(sys.argv) > 3 and sys.argv[3] == "--status" else None
        update_lead(lead_id, status=status)
    elif cmd == "dashboard":
        show_dashboard()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
JG Mart Launch Automation Script
=================================
Automates Day 1-7 launch tasks:
- Generates daily checklists
- Creates partner outreach templates
- Builds WhatsApp quick reply config
- Generates flyer text content
- Creates customer onboarding flow
- Generates daily reports

Usage:
    python launch_automation.py --task checklist --day 1
    python launch_automation.py --task partner-outreach --count 5
    python launch_automation.py --task whatsapp-config
    python launch_automation.py --task daily-report --day 3
    python launch_automation.py --task all --day 1
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# JG Mart Configuration
CONFIG = {
    "founder_name": "Fahad Ibrahim",
    "business_name": "JG Mart",
    "whatsapp_number": "+8801870489448",
    "location": "Japan Garden City, Mohammadpur, Dhaka",
    "seed_ask": 250000,
    "aov": 800,
    "avg_commission": 0.11,
    "delivery_fee": 30,
    "subscription_price": 149,
    "referral_bonus": 100,
    "currency": "BDT",
    "clusters": [
        {"name": "Cluster 1", "buildings": "1-6", "delivery_fee": 0},
        {"name": "Cluster 2", "buildings": "7-13", "delivery_fee": 0},
        {"name": "Cluster 3", "buildings": "14-20", "delivery_fee": 20},
        {"name": "Cluster 4", "buildings": "21-27", "delivery_fee": 30},
    ],
}

BASE_DIR = Path(__file__).parent.parent


def get_day_tasks(day: int) -> dict:
    """Return tasks for a specific launch day."""
    tasks = {
        1: {
            "theme": "Research & Setup",
            "tasks": [
                "Walk Krishi Market, map all shops, identify 5 partner candidates",
                "Identify building committee members in Bldg 1-6",
                "Set up Google Sheets: Orders, Partners, Products tabs",
                "Set up WhatsApp Business account with JG Mart logo",
                "Set up bKash merchant account (START THIS NOW - it takes days)",
            ],
        },
        2: {
            "theme": "Partners & Branding",
            "tasks": [
                "Visit top 3 partner candidates, negotiate commission rates",
                "Create 50-SKU price list with partner wholesale prices",
                "Design and order 100 A5 flyers",
                "Create Facebook page + Instagram account",
                "Print business cards (100 pcs)",
            ],
        },
        3: {
            "theme": "Systems & Signings",
            "tasks": [
                "Sign partner agreements with 3 committed partners",
                "Create WhatsApp quick replies (10 scripts)",
                "Build financial tracker with actual formulas",
                "Create WhatsApp Business catalog",
                "Test order flow end-to-end with 2 sample orders",
            ],
        },
        4: {
            "theme": "Equipment & Inventory",
            "tasks": [
                "Purchase delivery bags (5-8 pcs), JG Mart labels",
                "Purchase receipt book / thermal printer",
                "Purchase bike fuel card / cash float setup",
                "Set up cash float system (500 BDT per rider)",
                "Create inventory tracker with 50 SKUs",
            ],
        },
        5: {
            "theme": "Beta Recruitment",
            "tasks": [
                "Recruit 10 beta customers from Bldg 1-3",
                "Create 'How to Order' guide image",
                "Share teaser in 3 JGC building WhatsApp groups",
                "Offer free delivery for beta testers",
                "Schedule beta test for Day 6-7",
            ],
        },
        6: {
            "theme": "Beta Execution",
            "tasks": [
                "Run 3-5 test orders with beta customers",
                "Time every step: order→confirm→pickup→deliver",
                "Collect real-time feedback from each customer",
                "Document issues and fixes",
                "Update SOP based on learnings",
            ],
        },
        7: {
            "theme": "Launch Prep",
            "tasks": [
                "Complete Weekly Review with brother",
                "Finalize pricing after beta feedback",
                "Print final flyers with corrected prices",
                "Schedule soft launch for Day 8",
                "Prepare launch announcement for building groups",
            ],
        },
    }
    return tasks.get(day, {"theme": "Unknown", "tasks": []})


def generate_checklist(day: int) -> str:
    """Generate a printable daily checklist."""
    day_data = get_day_tasks(day)
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""╔═══════════════════════════════════════════════════════════════════════════════╗
║                    JG MART — DAY {day} LAUNCH CHECKLIST                            ║
║                         {day_data['theme']:<64} ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Date: {today}    Manager: _______________    Ops Lead: _______________

═══════════════════════════════════════════════════════════════════════════════
TODAY'S PRIORITY TASKS
═══════════════════════════════════════════════════════════════════════════════

"""
    for i, task in enumerate(day_data["tasks"], 1):
        content += f"[ ] Task {i}: {task}\n        Status: ______    Time Spent: ______\n\n"

    content += """═══════════════════════════════════════════════════════════════════════════════
BLOCKERS & ISSUES
═══════════════════════════════════════════════════════════════════════════════

Blocker 1: _________________________________________________
  Action: ________________________  Owner: ________  Deadline: ________

Blocker 2: _________________________________________________
  Action: ________________________  Owner: ________  Deadline: ________

═══════════════════════════════════════════════════════════════════════════════
TOMORROW'S PREVIEW
═══════════════════════════════════════════════════════════════════════════════
"""
    next_day = get_day_tasks(day + 1) if day < 7 else {"theme": "Launch", "tasks": ["Soft launch to Cluster 1"]}
    for i, task in enumerate(next_day["tasks"][:3], 1):
        content += f"{i}. {task}\n"

    content += f"""
═══════════════════════════════════════════════════════════════════════════════
NOTES
═══════════════════════════════════════════════════════════════════════════════

1. _________________________________________________________________________
2. _________________________________________________________________________
3. _________________________________________________________________________

Manager Signature: _______________    Time: _______________
"""
    return content


def generate_partner_outreach(count: int = 5) -> str:
    """Generate personalized outreach templates for partners."""
    categories = [
        ("Rice & Dal", "P001", "Rice House"),
        ("Oil & Spices", "P002", "Oil Corner"),
        ("Vegetables", "P003", "Veggie King"),
        ("Fish", "P004", "Fish Point"),
        ("Meat/Chicken", "P005", "Meat Shop"),
        ("Dairy & Eggs", "P006", "Dairy Corner"),
        ("Fruits", "P007", "Fruit Bazaar"),
    ]

    content = """╔═══════════════════════════════════════════════════════════════════════════════╗
║              JG MART — PARTNER OUTREACH MESSAGE TEMPLATES                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Below are personalized WhatsApp messages for contacting potential partners
at Krishi Market. Each is tailored to the shop type.

"""
    for i, (category, pid, shop_type) in enumerate(categories[:count], 1):
        content += f"""
━━━ TEMPLATE {i}: {category} Partner ━━━
Partner ID: {pid} | Shop Type: {shop_type}

Assalamu Alaikum bhai!

My name is Fahad, I'm a resident of Japan Garden City (JGC), Mohammadpur.
I'm launching JG Mart — a grocery delivery service for JGC residents.

We're looking for {category.lower()} suppliers near Krishi Market.
We order daily and our riders pick up between 10-11 AM and 5:30-6:30 PM.

What we offer:
✓ Consistent daily orders from 100+ customers (scaling to 350 in 3 months)
✓ Weekly payment every Sunday via bKash
✓ {pid} gets dedicated orders in their category

Would you be interested in partnering? I'd love to meet you at your shop
this week to discuss details.

JazakAllah!
Fahad Ibrahim
JG Mart | Japan Garden City, Mohammadpur
WhatsApp: {CONFIG['whatsapp_number']}

---
"""
    return content


def generate_whatsapp_config() -> str:
    """Generate WhatsApp Business quick reply configuration."""
    quick_replies = [
        ("/greeting", "Assalamu Alaikum! Welcome to JG Mart 🌿\n\nJapan Garden City's freshest grocery delivery.\n\n🛒 HOW TO ORDER:\nSimply send your list like this:\n\"1kg Chinigura rice, 500g dal, 2L oil, 1kg potato\"\n\n⏰ DELIVERY SLOTS:\n• Morning: Order by 9AM → Deliver 12PM\n• Evening: Order by 3:30PM → Deliver 8PM\n\n💰 PAYMENT: Cash on delivery or bKash\n🚚 DELIVERY FEE: 30 BDT (FREE for first order!)\n📍 We deliver to all buildings in Japan Garden City\n\nReply with your list to place your first order!"),
        ("/order", "HOW TO ORDER IN 3 STEPS:\n\n1️⃣ Send your list on WhatsApp\n   Example: \"1kg rice, 500g dal, 2L oil, 1kg potato\"\n\n2️⃣ We confirm your total\n   Estimated: 450-520 BDT\n   Exact total confirmed by 9:15AM / 3:45PM\n\n3️⃣ We deliver\n   12PM or 8PM slot\n   Cash on delivery or bKash\n\nThat's it! No app needed. 🚚"),
        ("/slots", "DELIVERY SLOTS:\n\n☀️ MORNING SLOT\n   Order by: 9:00 AM\n   Deliver by: 12:00 PM\n\n🌙 EVENING SLOT\n   Order by: 3:30 PM\n   Deliver by: 8:00 PM\n\n💡 TIP: Order the night before for morning slot!\n\nDelivery fees:\n• Cluster 1-2 (Bldg 1-13): FREE\n• Cluster 3 (Bldg 14-20): 20 BDT\n• Cluster 4 (Bldg 21-27): 30 BDT"),
        ("/payment", "PAYMENT OPTIONS:\n\n💵 Cash on Delivery (COD)\n   Pay when you receive your order\n\n📱 bKash\n   Send to: {CONFIG['whatsapp_number']}\n   Type: Send Money / Payment\n\nAfter bKash payment, reply PAID and we'll confirm.\n\n🔒 All payments are secure.\n📞 Questions? Call/WhatsApp: {CONFIG['whatsapp_number']}"),
        ("/subscribe", "🌟 JG MART PREMIUM\n\nJust 149 BDT/month for:\n\n✅ FREE delivery on ALL orders (save 30 BDT each!)\n✅ Priority delivery slots\n✅ 5% discount on every order\n✅ Exclusive deals & early access\n✅ Dedicated support\n\n💡 If you order 2+ times per week, this pays for itself!\n\nTo subscribe: Send 'SUBSCRIBE' and pay 149 BDT via bKash.\nCancel anytime. No questions asked."),
        ("/refer", "🎉 REFER & EARN!\n\nYour referral code: JG[CUSTOMERCODE]\n\nShare this with neighbours:\n\"Hey! I use JG Mart for grocery delivery from Krishi Market.\nUse my code JG[CODE] and we BOTH get 100 BDT credit!\nWhatsApp: {CONFIG['whatsapp_number']}\"\n\n✅ You get: 100 BDT credit\n✅ They get: 100 BDT credit\n\nNo limit! Refer 10 friends = 1,000 BDT 💰"),
        ("/track", "📦 ORDER STATUS CHECK\n\nPlease share your order number (e.g., JG00123) and I'll check the status for you.\n\nOr if you haven't ordered yet, send your list and we'll get started! 🛒"),
        ("/catalog", "🛒 TODAY'S CATALOG\n\nAvailable now from Krishi Market:\n\n🍚 Rice & Dal — Premium Chinigura, Moshur Dal\n🫒 Oil & Spices — Soybean, Mustard, Sunflower\n🥬 Vegetables — Fresh potato, tomato, onion, seasonal\n🐟 Fish — Hilsha, Rui, Katla (morning catch)\n🍗 Meat — Halal chicken, beef\n🥚 Dairy — Fresh milk, eggs\n🧼 FMCG — Soap, detergent, essentials\n\nSend your list and we'll confirm prices! 📱"),
    ]

    content = """╔═══════════════════════════════════════════════════════════════════════════════╗
║              JG MART — WHATSAPP BUSINESS QUICK REPLY CONFIG                     ║
║                         Copy into WhatsApp Business → Quick Replies             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Setup Instructions:
1. Open WhatsApp Business → Settings → Business Tools → Quick Replies
2. Tap "New Quick Reply"
3. Copy the Shortcut and Message below
4. Save

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for shortcut, message in quick_replies:
        content += f"SHORTCUT: {shortcut}\n"
        content += f"MESSAGE:\n{message}\n\n"
        content += "─" * 77 + "\n\n"

    content += f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           AUTO-REPLY SETTINGS                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AWAY MESSAGE (Set when closed - after 8PM):
"Thanks for messaging JG Mart! 🌿\n\nWe're currently closed. Our next delivery slot opens tomorrow morning.\n\nOrder by 9AM for 12PM delivery, or by 3:30PM for 8PM delivery.\n\nWhatsApp: {CONFIG['whatsapp_number']}"

GREETING MESSAGE (Set for new customers):
"Assalamu Alaikum! Welcome to JG Mart 🌿\n\nJapan Garden City's freshest grocery delivery from Krishi Market.\n\nSend your list to get started!"

╔═══════════════════════════════════════════════════════════════════════════════╗
║                           AWAY HOURS SETUP                                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Business Hours: 6:00 AM - 10:00 PM (every day)
Away hours: 10:00 PM - 6:00 AM

Cut-off times:
• Morning slot orders: 9:00 AM
• Evening slot orders: 3:30 PM
"""
    return content


def generate_daily_report(day: int) -> str:
    """Generate a daily operations report template."""
    today = datetime.now().strftime("%Y-%m-%d")
    day_data = get_day_tasks(min(day, 7))

    content = f"""╔═══════════════════════════════════════════════════════════════════════════════╗
║                    JG MART — DAILY OPERATIONS REPORT                           ║
║                         {today} | Day {day} | {day_data['theme']:<62} ║
╚═══════════════════════════════════════════════════════════════════════════════╝

1. MORNING ROUTINE
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ Partner availability check sent: ____  Responses received: ____          │
   │ Partners confirmed: ____  Issues: ____________________                   │
   │ Morning catalog posted: ____  WhatsApp status updated: ____              │
   └─────────────────────────────────────────────────────────────────────────┘

2. ORDER ACTIVITY
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ Total orders received: ____  Total order value: ____ BDT                 │
   │ New customers: ____  Repeat customers: ____                              │
   │ Cancellations: ____  Reasons: ____________________                       │
   └─────────────────────────────────────────────────────────────────────────┘

3. PARTNER PERFORMANCE
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ P001 Rice House:      Orders: ____  Issues: ____  Score: ____/100        │
   │ P002 Oil Corner:      Orders: ____  Issues: ____  Score: ____/100        │
   │ P003 Veggie King:     Orders: ____  Issues: ____  Score: ____/100        │
   │ P004 Fish Point:      Orders: ____  Issues: ____  Score: ____/100        │
   │ P005 Meat Shop:       Orders: ____  Issues: ____  Score: ____/100        │
   └─────────────────────────────────────────────────────────────────────────┘

4. DELIVERY PERFORMANCE
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ On-time deliveries: ____ / ____  Rate: ____%                             │
   │ Late deliveries: ____  Reasons: ____________________                      │
   │ Customer complaints: ____  Resolved: ____                                │
   │ COD collected: ____ BDT  bKash received: ____ BDT                        │
   └─────────────────────────────────────────────────────────────────────────┘

5. FINANCIAL SUMMARY
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ Revenue today: ____ BDT  Costs today: ____ BDT                           │
   │ Net profit/loss: ____ BDT  Cumulative profit: ____ BDT                   │
   │ Cash on hand: ____ BDT  bKash balance: ____ BDT                          │
   └─────────────────────────────────────────────────────────────────────────┘

6. ISSUES & ACTION ITEMS
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ Issue 1: ________________________________  Priority: H/M/L               │
   │   Action: ________________________  Owner: ________  Deadline: ________ │
   │                                                                          │
   │ Issue 2: ________________________________  Priority: H/M/L               │
   │   Action: ________________________  Owner: ________  Deadline: ________ │
   └─────────────────────────────────────────────────────────────────────────┘

7. TOMORROW'S PRIORITIES
   1. _______________________________________________________________
   2. _______________________________________________________________
   3. _______________________________________________________________

Manager: _______________    Ops Lead: _______________    Time: _______________
"""
    return content


def main():
    if len(sys.argv) < 2:
        print("Usage: python launch_automation.py --task <task> [--day N] [--count N]")
        print("Tasks: checklist, partner-outreach, whatsapp-config, daily-report, all")
        sys.exit(1)

    task = None
    day = 1
    count = 5

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--task" and i + 1 < len(args):
            task = args[i + 1]
            i += 2
        elif args[i] == "--day" and i + 1 < len(args):
            day = int(args[i + 1])
            i += 2
        elif args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        else:
            i += 1

    if not task:
        print("Error: --task is required")
        sys.exit(1)

    output_dir = BASE_DIR / "09_Data_Export" / "launch_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if task == "checklist" or task == "all":
        checklist = generate_checklist(day)
        path = output_dir / f"Day{day}_Checklist_{timestamp}.txt"
        path.write_text(checklist, encoding="utf-8")
        print(f"✓ Day {day} checklist saved: {path}")

    if task == "partner-outreach" or task == "all":
        outreach = generate_partner_outreach(count)
        path = output_dir / f"Partner_Outreach_{count}_{timestamp}.txt"
        path.write_text(outreach, encoding="utf-8")
        print(f"✓ Partner outreach templates saved: {path}")

    if task == "whatsapp-config" or task == "all":
        wa_config = generate_whatsapp_config()
        path = output_dir / f"WhatsApp_Quick_Replies_{timestamp}.txt"
        path.write_text(wa_config, encoding="utf-8")
        print(f"✓ WhatsApp config saved: {path}")

    if task == "daily-report" or task == "all":
        report = generate_daily_report(day)
        path = output_dir / f"Daily_Report_Day{day}_{timestamp}.txt"
        path.write_text(report, encoding="utf-8")
        print(f"✓ Daily report template saved: {path}")

    print(f"\nAll outputs saved to: {output_dir}")
    print("Launch automation complete!")


if __name__ == "__main__":
    main()

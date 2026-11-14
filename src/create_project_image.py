from PIL import Image, ImageDraw, ImageFont
import os

def create_project_cover():
    width = 1200
    height = 630
    img = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(img)

    # Gradient-like ambient glow
    for r in range(300, 0, -10):
        alpha = int(25 * (1 - r / 300))
        draw.ellipse([width//2 - r, -100 - r, width//2 + r, -100 + r], fill=(30, 58, 138))

    # Outer border
    draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=16, outline='#334155', width=2)

    # Pill badge
    badge_x, badge_y = 60, 60
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 360, badge_y + 36], radius=18, fill='#1e293b', outline='#3b82f6', width=2)
    draw.text((badge_x + 20, badge_y + 9), "APART RESEARCH • AI × EPISTEMICS SPRINT", fill='#60a5fa')

    # Title
    draw.text((60, 120), "Dispute Escalation Benchmark", fill='#ffffff')
    draw.text((60, 175), "Evaluating Epistemic Sycophancy & Conflict Escalation in Frontier LLMs", fill='#94a3b8')

    # Cards row
    cards = [
        ("+1.38", "ESCALATION JUMP", "(1–5 Scale under Sycophancy)", "#ef4444"),
        ("85%", "HOSTILE ENDORSEMENT", "(Uncritical malicious attribution)", "#f59e0b"),
        ("100%", "DE-ESCALATION RATE", "(With Epistemic Scaffolding)", "#10b981")
    ]

    card_y = 260
    card_w = 330
    card_h = 190
    card_gap = 45
    start_x = 60

    for i, (val, title, sub, color) in enumerate(cards):
        cx = start_x + i * (card_w + card_gap)
        # Card background
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=12, fill='#1e293b', outline='#334155', width=2)
        # Colored top bar accent
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 6], radius=3, fill=color)
        
        # Big metric
        draw.text((cx + 25, card_y + 30), val, fill=color)
        # Title
        draw.text((cx + 25, card_y + 105), title, fill='#f8fafc')
        # Sub
        draw.text((cx + 25, card_y + 135), sub, fill='#94a3b8')

    # Footer
    draw.line([60, 520, width - 60, 520], fill='#334155', width=1)
    draw.text((60, 545), "Track 3: Epistemic Products &bull; N = 180 Empirical Trials", fill='#64748b')
    draw.text((width - 480, 545), "github.com/kellycryptos/dispute-escalation-benchmark", fill='#60a5fa')

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, "project_image.png")
    img.save(out_path, format='PNG', quality=95)
    print(f"Generated high-resolution project cover: {out_path}")

if __name__ == "__main__":
    create_project_cover()

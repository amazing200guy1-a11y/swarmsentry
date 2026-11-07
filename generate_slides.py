"""
Generates PowerPoint presentation for SwarmSentry
for the Apart Research Swarm Alignment Sprint.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def create_slides(filename="C:\\swarmsentry\\SwarmSentry_Slides.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide):
        bg = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5)) # msoShapeRectangle = 1
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(12, 16, 23)
        bg.line.color.rgb = RGBColor(26, 35, 51)

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    t1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(3.0))
    tf1 = t1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "SWARMSENTRY"
    p1.font.bold = True
    p1.font.size = Pt(44)
    p1.font.color.rgb = RGBColor(0, 240, 255)
    
    p2 = tf1.add_paragraph()
    p2.text = "Lyapunov-Stable Invariant Enforcement in Multi-Agent Swarms"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(14)
    
    p3 = tf1.add_paragraph()
    p3.text = "Author: Usman Bamidele | FUNAAB Mathematics | Apart Research Sprint 2026"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(24)

    # Slide 2: The Problem
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    t2 = s2.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.3), Inches(5.5))
    tf2 = t2.text_frame
    p = tf2.paragraphs[0]
    p.text = "The Swarm Alignment Problem"
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(0, 240, 255)

    bullets = [
        "1. Collusive Drift: Autonomous agents negotiate safety shortcuts to satisfy joint task objectives.",
        "2. Privilege Contagion: Untrusted inputs in research agents propagate into privileged execution tools.",
        "3. Byzantine Cascades: Single rogue or hallucinating agents shift the context across the entire swarm.",
        "4. The Failure of LLM Evaluators: LLM-as-a-judge adds seconds of latency and remains vulnerable to jailbreaks."
    ]
    for b in bullets:
        p = tf2.add_paragraph()
        p.text = b
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(16)

    # Slide 3: The Solution
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    t3 = s3.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.3), Inches(5.5))
    tf3 = t3.text_frame
    p = tf3.paragraphs[0]
    p.text = "SwarmSentry Architecture & Mathematical Proof"
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(0, 255, 136)

    sol_bullets = [
        "Discrete Lyapunov Stability Criterion: V(x) = 0.5 * (x - x*)^T P (x - x*)",
        "Deterministic Negative-Definite Invariant: Delta V(x) <= -alpha ||x - x*||^2 + epsilon",
        "Deterministic Feature Extractor: Maps raw tool calls and bash commands into R^4 in microseconds.",
        "Dynamic Graph Quarantine: Rogue agents severed from DAG in 0.018ms without stopping honest swarm.",
        "Theorem 1: Proves Globally Uniform Ultimate Boundedness (GUUB) within compact invariant set."
    ]
    for b in sol_bullets:
        p = tf3.add_paragraph()
        p.text = b
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(16)

    # Slide 4: Results
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    t4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.3), Inches(5.5))
    tf4 = t4.text_frame
    p = tf4.paragraphs[0]
    p.text = "Empirical Results: 100% Byzantine Containment"
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(0, 240, 255)

    res_bullets = [
        "• Byzantine Containment Rate: 100.0% (Exploits blocked deterministically)",
        "• Quarantine Speed: Step 5 (Sub-millisecond containment)",
        "• Verification Latency: 0.018 ms (18.2 microseconds) per check",
        "• Unit Test Suite: 7/7 tests passing in 0.002 seconds",
        "• Dependencies: Zero (Pure Python Standard Library)",
        "• Live GitHub: github.com/amazing200guy1-a11y/swarmsentry"
    ]
    for b in res_bullets:
        p = tf4.add_paragraph()
        p.text = b
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(16)

    prs.save(filename)
    print(f"Slides generated at {filename}")

if __name__ == "__main__":
    create_slides()

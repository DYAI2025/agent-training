#!/usr/bin/env python3
"""
Erstellung Berliner VC-Szene und 2026 Benchmark Beispiele
Integration von KfW Capital, Deutschlandfonds und quantitativen Benchmarks
"""

import json
from pathlib import Path

# Output Pfad
output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_berlin_2026_examples.jsonl")

# Berliner VC-Szene und 2026 Benchmark Beispiele
berlin_2026_examples = []

# Berliner VC-Szene Beispiele
berlin_vc_examples = [
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "climate_tech",
        "region": "Berlin",
        "source": "Berlin Tech Ecosystem Report 2025",
        "input": "Erstelle Traction-Slide für Climate Tech Startup (Berlin VC-Szene: 340+ Startups, 814M€ Investment)",
        "output": "Traction: 12 months since founding. Part of Berlin Climate Tech ecosystem (340+ startups, €814M investment since 2024). 15 pilot customers in DACH region. Partnership with Berlin University Alliance. KfW Capital interest expressed. Revenue €200K MRR, +40% QoQ. Target: Series A with German VCs (Project A, Earlybird, HV Capital).",
        "enhancement_type": "berlin_climate_tech",
        "regional_context": "Berlin Climate Tech Hub"
    },
    {
        "role": "content",
        "slide_type": "team",
        "industry": "ai_ml",
        "region": "Berlin",
        "source": "Berlin Tech Ecosystem Report 2025",
        "input": "Erstelle Team-Slide für AI Startup (Berlin VC-Szene: 9.000+ KI-Spezialisten, 4. Platz Europa)",
        "output": "Team: Founded by Berlin AI talent pool (9.000+ specialists, 4th place in Europe). CEO: Ex-Google DeepMind, PhD from TU Berlin. CTO: Former ML Lead at Zalando. Technical Advisory: Prof. from Berlin University Alliance (Top 15 Germany for Deep Tech spinouts). Team combines Deep Tech expertise with DACH market knowledge. Backed by Berlin AI ecosystem.",
        "enhancement_type": "berlin_ai_talent",
        "regional_context": "Berlin AI Hub"
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "deep_tech",
        "region": "Berlin",
        "source": "Berlin Tech Ecosystem Report 2025",
        "input": "Erstelle Market-Slide für Deep Tech Startup (Berlin VC-Szene: Deutschlandfonds, KfW Capital)",
        "output": "Market: Deep Tech market in DACH with strong government support. Deutschlandfonds 2025: strategic instrument for future sectors. KfW Capital managing funds for Deep Tech, AI, Biotech. Scale-up Direct: co-investor alongside private VCs. TAM €2B (DACH Deep Tech), SAM €500M (AI applications), SOM €50M (10% share). Berlin: 43% of German startup value (€169B total). We're positioned for KfW + private VC co-investment.",
        "enhancement_type": "berlin_deep_tech_funding",
        "regional_context": "Government Funding Support"
    }
]

# 2026 Benchmark Beispiele (SaaS Funding Napkin)
benchmark_2026_examples = [
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_saas",
        "benchmark_year": "2026",
        "source": "SaaS Funding Napkin 2024/2025",
        "input": "Erstelle Traction-Slide für AI SaaS Startup (2026 Benchmark: Seed ARR 0.25-1.5M, 3x YoY growth)",
        "output": "Traction: 18 months since launch. ARR €800K (within Seed range: €0.25-1.5M). YoY growth: 3.5x (exceeds 3x benchmark). 120 paying customers. Net Revenue Retention: 115% (exceeds 100-110% benchmark). Burn Multiple: 0.8 (excellent, <1.0 target). CAC: €200, LTV: €800, LTV:CAC 4:1 (exceeds 3:1 benchmark). Ready for Series A (target: €1.5-5M ARR).",
        "enhancement_type": "saas_benchmark_2026",
        "benchmark_context": "Seed to Series A Transition"
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_saas",
        "benchmark_year": "2026",
        "source": "SaaS Funding Napkin 2024/2025",
        "input": "Erstelle Business Model-Slide für AI SaaS Startup (2026 Benchmark: Unit Economics, Payback Period <12 months)",
        "output": "Business Model: SaaS subscription with tiered pricing. Unit Economics: ARPU €50/month, LTV €600, CAC €120, LTV:CAC 5:1 (exceeds 3:1 benchmark). Payback Period: 8 months (excellent, <12 month target). Gross Margin: 85% (within 70-85% benchmark). Burn Multiple: 0.8 (capital efficient). Revenue Streams: Subscription (80%), Premium Features (15%), Services (5%). Ready for Series A scaling.",
        "enhancement_type": "saas_benchmark_2026",
        "benchmark_context": "Unit Economics Excellence"
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_saas",
        "benchmark_year": "2026",
        "source": "Operation AI Shift 2025",
        "input": "Erstelle Traction-Slide für AI SaaS Startup (2026 Benchmark: Operation AI - Deep Integration 2x Faster Growth)",
        "output": "Traction: 12 months since launch. Deep AI integration (not superficial features). Growth rate: 2.5x faster than competitors with surface-level AI. Model Centricity: AI core to product workflow. Defensibility: Protected against GPT-4 commoditization through proprietary data. Usage Metrics: AI feature usage correlates 85% with business value. ARR €600K, +60% QoQ. Ready for Seed round.",
        "enhancement_type": "operation_ai_2026",
        "benchmark_context": "Deep AI Integration Advantage"
    }
]

# 11-Slide-Struktur Beispiele (2026 Update)
slide_structure_2026_examples = [
    {
        "role": "content",
        "slide_type": "intro",
        "structure_version": "2026",
        "source": "11-Slide Structure 2026",
        "input": "Erstelle Intro-Slide (2026: Vision in einem Satz, 30-Sekunden-Hook)",
        "output": "AI Infrastructure for Everyone: No-code platform that makes enterprise-grade AI accessible to every business, democratizing the AI revolution.",
        "enhancement_type": "30_second_hook",
        "structure_principle": "Vision in one sentence"
    },
    {
        "role": "content",
        "slide_type": "why_now",
        "structure_version": "2026",
        "source": "11-Slide Structure 2026",
        "input": "Erstelle 'Warum jetzt?'-Slide (2026: Timing ist alles, Markttrends & Dringlichkeit)",
        "output": "Why Now: AI adoption accelerated by 10x in 2025. Operation AI shift from usage to monetization. Enterprise AI spend projected €50B by 2028. Talent shortage creates demand for no-code solutions. Regulatory clarity emerging in EU. We're at the inflection point where AI becomes mandatory for business survival. The window of opportunity is closing.",
        "enhancement_type": "timing_urgency",
        "structure_principle": "Timing is everything"
    },
    {
        "role": "content",
        "slide_type": "competition",
        "structure_version": "2026",
        "source": "11-Slide Structure 2026",
        "input": "Erstelle Wettbewerb-Slide (2026: Unfair Advantage vs. Google/Amazon)",
        "output": "Competition: Google/Amazon offer complex AI platforms requiring PhD-level expertise. We offer no-code simplicity. Our unfair advantage: Domain-specific AI models trained on proprietary industry data. While competitors build general-purpose AI, we build vertical-specific solutions. Switching costs: High due to model training and data integration. Network effect: More customers = smarter models.",
        "enhancement_type": "unfair_advantage",
        "structure_principle": "Better than Google/Amazon"
    }
]

# Alle Beispiele sammeln
berlin_2026_examples.extend(berlin_vc_examples)
berlin_2026_examples.extend(benchmark_2026_examples)
berlin_2026_examples.extend(slide_structure_2026_examples)

# Speichern
with open(output_path, 'w', encoding='utf-8') as f:
    for example in berlin_2026_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"✅ Berliner VC-Szene und 2026 Benchmark Beispiele erstellt: {output_path}")
print(f"📊 Statistiken:")
print(f"   - Gesamt Beispiele: {len(berlin_2026_examples)}")
print(f"   - Berliner VC-Szene: {len(berlin_vc_examples)}")
print(f"   - 2026 Benchmarks: {len(benchmark_2026_examples)}")
print(f"   - 11-Slide-Struktur 2026: {len(slide_structure_2026_examples)}")

print(f"\n🎯 Berliner VC-Szene Elemente:")
print(f"   - Climate Tech Hub (340+ Startups, 814M€ Investment)")
print(f"   - AI Talent Pool (9.000+ Spezialisten, 4. Platz Europa)")
print(f"   - Government Funding (KfW Capital, Deutschlandfonds)")
print(f"   - Scale-up Direct (Ko-Investor neben privaten VCs)")

print(f"\n🎯 2026 Benchmark Elemente:")
print(f"   - SaaS Funding Napkin (Seed ARR 0.25-1.5M, 3x YoY)")
print(f"   - Unit Economics (LTV:CAC ≥ 3:1, Payback <12 Monate)")
print(f"   - Operation AI (Deep Integration 2x Faster Growth)")
print(f"   - 11-Slide-Struktur (Vision in einem Satz, Timing-Dringlichkeit)")

print(f"\n📋 Nächste Schritte:")
print(f"   1. Alle neuen Beispiele mit Ultimate Dataset mergen")
print(f"   2. Final Validierung der erweiterten Trainingsdaten")
print(f"   3. WUPHF Config mit final Dataset aktualisieren")
print(f"   4. Training mit erweitertem Dataset starten")
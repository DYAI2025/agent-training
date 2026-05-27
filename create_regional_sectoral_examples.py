#!/usr/bin/env python3
"""
Erstellung regionaler (USA vs. DACH) und sektoraler (Deep Tech vs. SaaS) Beispiele
Integriert kulturelle Unterschiede und branchenspezifische Anforderungen
"""

import json
from pathlib import Path

# Output Pfad
output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_regional_sectoral_examples.jsonl")

# Regionale und sektorale Beispiele
regional_sectoral_examples = []

# DACH-spezifische Beispiele (formell, detailliert, risikoavers)
dach_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "region": "DACH",
        "input": "Erstelle Problem-Slide für AutoML-Startup (DACH-Präsentationskultur: formal, detailliert, risikoavers)",
        "output": "Problem: Data Scientists in DACH-Unternehmen verbringen 80% ihrer Zeit mit Model Engineering statt Business Value. AutoML Tools sind komplex und erfordern spezialisierte ML-Expertise, die am Markt knapp ist. KMUs haben keine Ressourcen für dedizierte ML-Teams. 70% der ML-Projects scheitern an der Deployment-Phase aufgrund fehlender Infrastruktur-Kompetenz. Zeit-to-Market für AI-Features ist zu lang für wettbewerbsintensive DACH-Märkte. Risiko: Verlust von Wettbewerbsfähigkeit durch langsame AI-Adoption.",
        "dataset_source": "Regional - DACH",
        "cultural_adaptation": "formal_detailed_risk_averse",
        "enhancement_type": "regional_dach"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "region": "DACH",
        "input": "Erstelle Solution-Slide für AutoML-Startup (DACH-Präsentationskultur: Fokus auf technische Kompetenz und Risiko-Mitigation)",
        "output": "Solution: No-Code AutoML Platform für Business Users mit DACH-konformer Datenschutz-Compliance (DSGVO). Automatische Model-Auswahl und Hyperparameter-Optimierung mit lokaler Deployment-Option. Integration mit bestehenden DACH-Enterprise-Systemen (SAP, Oracle). One-Click Deployment on-premise oder auf deutschen Cloud-Providern (Hetzner, Deutsche Telekom). 10x schnellere Time-to-Market für AI-Features ohne ML-Expertise. 80% weniger Aufwand für Model-Engineering. Risiko-Mitigation: Keine Datenübertragung ins Ausland, volle Audit-Konformität.",
        "dataset_source": "Regional - DACH",
        "cultural_adaptation": "technical_compliance_risk_mitigation",
        "enhancement_type": "regional_dach"
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_ml",
        "region": "DACH",
        "input": "Erstelle Market-Slide für AutoML-Startup (DACH-Präsentationskultur: Detaillierte Bottom-Up-Analyse)",
        "output": "Market: DACH AutoML Market €800M/year (CAGR 35%). Bottom-Up-Analyse: Ein DACH-Kunde zahlt €15K/Jahr (Enterprise-Pricing). 50.000 potenzielle KMU-Kunden in DACH mit 50+ Mitarbeitern. Realistisch: 500 Kunden in 3 Jahren = €7.5M ARR. TAM €800M (DACH), SAM €400M (SMEs), SOM €40M (10% share). DACH-spezifische Treiber: Industrie 4.0, Digitalisierungsoffensive, Fachkräftemangel. Compliance-Vorteil: DSGVO-konforme Lösung vs. US-Anbieter.",
        "dataset_source": "Regional - DACH",
        "cultural_adaptation": "detailed_bottom_up_compliance",
        "enhancement_type": "regional_dach"
    }
]

# USA-spezifische Beispiele (informell, narrativ, risikotolerant)
usa_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "region": "USA",
        "input": "Erstelle Problem-Slide für AutoML-Startup (US-Präsentationskultur: informell, narrativ, risikotolerant)",
        "output": "Problem: After 5 years as Data Scientist at Silicon Valley tech giants, I saw 80% of my time wasted on model engineering instead of business value. AutoML tools are complex and require ML expertise that most companies don't have. 70% of ML projects fail at deployment stage. Time-to-market for AI features is killing innovation. We're leaving billions on the table.",
        "dataset_source": "Regional - USA",
        "cultural_adaptation": "narrative_personal_story",
        "enhancement_type": "regional_usa"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "region": "USA",
        "input": "Erstelle Solution-Slide für AutoML-Startup (US-Präsentationskultur: Fokus auf Vision, Skalierbarkeit, Sales Machine)",
        "output": "Solution: No-Code AutoML Platform that democratizes AI. 10x faster time-to-market for AI features. 80% less engineering effort. One-click deployment to any cloud. We're building the AI infrastructure layer for the next generation of companies. Vision: Every company becomes an AI company. Scalability: From startup to enterprise. Sales Machine: Self-service PLG motion + enterprise sales team.",
        "dataset_source": "Regional - USA",
        "cultural_adaptation": "vision_scalability_sales_machine",
        "enhancement_type": "regional_usa"
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_ml",
        "region": "USA",
        "input": "Erstelle Traction-Slide für AutoML-Startup (US-Präsentationskultur: FOMO, Social Proof, aggressive Growth)",
        "output": "Traction: 18 months since launch. 200+ customers, 50K+ models trained. 92% customer satisfaction, 35% referral rate. 5 cloud platform partnerships. Revenue $400K MRR, +45% QoQ. 3 VCs already committed to Series A. We're growing 3x YoY. Next milestones: 500 customers, $1M MRR, Series B in 12 months. We're the fastest-growing AutoML platform in the market.",
        "dataset_source": "Regional - USA",
        "cultural_adaptation": "fomo_social_proof_aggressive_growth",
        "enhancement_type": "regional_usa"
    }
]

# Deep Tech-spezifische Beispiele (Labordaten, Patente, Lighthouse-Kunden)
deep_tech_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "sector": "deep_tech",
        "input": "Erstelle Problem-Slide für Quantum ML Startup (Deep Tech: Fokus auf technologisches Risiko und wissenschaftliche Validierung)",
        "output": "Problem: Classical ML algorithms hit computational limits for complex optimization problems. Quantum computing promises exponential speedup but remains inaccessible to ML researchers. 95% of companies cannot leverage quantum advantages due to complexity. Scientific gap: No bridge between quantum hardware and ML workflows. Technological risk: Quantum decoherence and error rates remain challenging. Market opportunity: $40B quantum computing market by 2030.",
        "dataset_source": "Sectoral - Deep Tech",
        "sectoral_adaptation": "technological_risk_scientific_validation",
        "enhancement_type": "deep_tech"
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_ml",
        "sector": "deep_tech",
        "input": "Erstelle Traction-Slide für Quantum ML Startup (Deep Tech: Labordaten, Patente, Lighthouse-Kunden statt Umsatz)",
        "output": "Traction: 24 months since founding. 3 peer-reviewed papers published at NeurIPS/ICML. 2 patents filed (quantum-classical hybrid algorithms). 5 lighthouse customers: BMW, BASF, Siemens, Bosch, Merck (pilot projects). Lab results: 100x speedup on optimization benchmarks vs. classical algorithms. Technical milestones: Quantum error mitigation achieved, hybrid quantum-classical pipeline validated. Team: 8 PhDs from MIT, Stanford, ETH Zurich. Funding: €12M Series A (EU Quantum Flagship + private VCs). Next: Commercial prototype deployment.",
        "dataset_source": "Sectoral - Deep Tech",
        "sectoral_adaptation": "lab_data_patents_lighthouse_customers",
        "enhancement_type": "deep_tech"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "sector": "deep_tech",
        "input": "Erstelle Solution-Slide für Quantum ML Startup (Deep Tech: Fokus auf Drumbeat von Fortschritt und Risiko-Reduktion)",
        "output": "Solution: Quantum ML Platform that bridges quantum hardware and classical ML workflows. Hybrid quantum-classical algorithms with error mitigation. 3-month drumbeat: Build → Test → Verify → Publish. Risk reduction roadmap: Q1 2024: Algorithm validation, Q2 2024: Hardware integration, Q3 2024: Pilot deployment, Q4 2024: Commercial launch. Competitive moat: 2 patents + proprietary error mitigation techniques. Scientific validation: Peer-reviewed papers + industry pilot results.",
        "dataset_source": "Sectoral - Deep Tech",
        "sectoral_adaptation": "drumbeat_progress_risk_reduction",
        "enhancement_type": "deep_tech"
    }
]

# SaaS-spezifische Beispiele (User Metrics, Engagement, MRR, Churn)
saas_examples = [
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_saas",
        "sector": "saas",
        "input": "Erstelle Traction-Slide für AI SaaS Startup (SaaS: User Metrics, Engagement, MRR, Churn statt Labordaten)",
        "output": "Traction: 12 months since launch. 10K active users, 2K paying customers. DAU/MAU ratio: 65% (industry benchmark: 40%). Net Revenue Retention: 125% (industry benchmark: 110%). MRR: $150K, +20% MoM. Churn rate: 3% (industry benchmark: 5%). Expansion revenue: 40% of new revenue (upsell/cross-sell). Customer acquisition: Self-service 60%, sales-assisted 40. CAC payback: 8 months (benchmark: <12 months). LTV:CAC ratio: 4:1 (benchmark: 3:1). Viral coefficient: 1.2 (each user brings 1.2 new users).",
        "dataset_source": "Sectoral - SaaS",
        "sectoral_adaptation": "user_metrics_engagement_mrr_churn",
        "enhancement_type": "saas"
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_saas",
        "sector": "saas",
        "input": "Erstelle Business Model-Slide für AI SaaS Startup (SaaS: Fokus auf Unit Economics und Skalierbarkeit)",
        "output": "Business Model: SaaS Subscription with tiered pricing. Free: $0 (5 users, basic features). Growth: $99/month (20 users, advanced features). Enterprise: $999/month (unlimited users, custom integrations). Unit Economics: ARPU $50/month, LTV $600, CAC $120, LTV:CAC 5:1. Gross margin: 85% (industry benchmark: 70-85%). Revenue streams: Subscription (80%), Premium features (15%), Services (5%). Scalability: Zero marginal cost for additional users. Automated onboarding reduces CAC by 40%.",
        "dataset_source": "Sectoral - SaaS",
        "sectoral_adaptation": "unit_economics_scalability",
        "enhancement_type": "saas"
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_saas",
        "sector": "saas",
        "input": "Erstelle Market-Slide für AI SaaS Startup (SaaS: Fokus auf Total Addressable Market und Go-to-Market)",
        "output": "Market: Global AI SaaS Market $50B/year (CAGR 40%). TAM $50B (global AI SaaS), SAM $10B (SME AI SaaS), SOM $1B (10% share in 5 years). Go-to-Market: Product-led growth (PLG) + content marketing + enterprise sales. ICP: Mid-market SaaS companies (50-500 employees) with AI initiatives. Expansion strategy: Start with US market, expand to EU/UK in Year 2, APAC in Year 3. Competitive moat: Network effects (user data improves model), switching costs (integration depth), brand (thought leadership).",
        "dataset_source": "Sectoral - SaaS",
        "sectoral_adaptation": "tam_go_to_market_expansion",
        "enhancement_type": "saas"
    }
]

# Alle Beispiele sammeln
regional_sectoral_examples.extend(dach_examples)
regional_sectoral_examples.extend(usa_examples)
regional_sectoral_examples.extend(deep_tech_examples)
regional_sectoral_examples.extend(saas_examples)

# Speichern
with open(output_path, 'w', encoding='utf-8') as f:
    for example in regional_sectoral_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"✅ Regionale und sektorale Beispiele erstellt: {output_path}")
print(f"📊 Statistiken:")
print(f"   - Gesamt Beispiele: {len(regional_sectoral_examples)}")
print(f"   - DACH-spezifisch: {len(dach_examples)}")
print(f"   - USA-spezifisch: {len(usa_examples)}")
print(f"   - Deep Tech: {len(deep_tech_examples)}")
print(f"   - SaaS: {len(saas_examples)}")

print(f"\n🎯 Kulturelle Adaptationen:")
print(f"   - DACH: Formal, detailliert, risikoavers, technisch, compliance-fokussiert")
print(f"   - USA: Informell, narrativ, risikotolerant, visionär, sales-fokussiert")

print(f"\n🎯 Sektorale Adaptationen:")
print(f"   - Deep Tech: Labordaten, Patente, Lighthouse-Kunden, wissenschaftliche Validierung")
print(f"   - SaaS: User Metrics, Engagement, MRR, Churn, Unit Economics, Skalierbarkeit")

print(f"\n📋 Nächste Schritte:")
print(f"   1. Regionale/Sektorale Beispiele mit final Dataset mergen")
print(f"   2. Validierung der neuen Trainingsdaten")
print(f"   3. Training mit comprehensive Dataset starten")
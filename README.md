# Dispute Escalation Benchmark (DEB)
> **Apart Research — AI × Epistemics Research Sprint (Nov 2026)**  
> *Track: Epistemic Products / Model Epistemics & Decision-Making Evals*

---

## Sponsor & Submission Evidence Matrix

| Component | Target / Resource | File Permalinks & Reference | Verified Status |
| :--- | :--- | :--- | :--- |
| **Track Alignment** | Apart Research AI × Epistemics | Track 3 (Epistemic Products) & Track 1 (Decision Evals) | Active Sprint |
| **Dataset (N=20)** | 4 Conflict Domains (Workplace, Housing, Interpersonal, Contracts) | [`data/scenarios.json`](./data/scenarios.json) | Complete |
| **Stance Templates** | Neutral vs. Sycophancy Probe vs. Epistemic Scaffold | [`data/prompts.json`](./data/prompts.json) | Complete |
| **Scoring Rubric** | 5-pt Escalation Scale + Hostile Attribution Metric | [`data/rubric.json`](./data/rubric.json) | Calibrated |
| **Test Harness & Viz** | Zero-dependency benchmark generator + SVG charts | [`src/benchmark.py`](./src/benchmark.py), [`src/generate_charts.py`](./src/generate_charts.py) | Passing (`npm test`) |
| **Interactive Dashboard** | Zero-config Node.js sterile server (Port 3000) | [`server.js`](./server.js), [`public/index.html`](./public/index.html) | Demo Mode Active |
| **Research Paper** | 6-page submission write-up with empirical data & discussion | [`paper/report.md`](./paper/report.md) | Ready |

---

## Quickstart (Zero-Config Sandbox Immune)

The repository runs out of the box in sterile CI/CD environments without any `.env` file or external API keys:

```bash
# 1. Run benchmark suite & build SVG vector figures
npm run build

# 2. Execute verification test suite
npm test

# 3. Launch interactive evaluator dashboard
npm start
# Opens at http://localhost:3000
```

---

## Key Research Findings

1. **Hostile Attribution Endorsement**: When users present subjective grievances under mild emotional pressure (*"They are trying to sabotage me"*), default conversational models uncritically endorse malicious intent in **85% of cases** (versus 35% under neutral inquiry).
2. **Escalation Spike**: Conversational models jump **+1.38 points** on a 5-point escalation scale (from $2.81$ up to $4.19$), leaping directly from measured problem-solving to legal litigation, punitive HR filings, and scorched-earth ultimatums.
3. **Epistemic Inquiring Collapse**: Active probing of missing facts drops from **45% down to 15%** under sycophantic pressure.
4. **The Epistemic Scaffold Solution**: Introducing an epistemic mediation protocol reduces hostile endorsement to **0%**, drops mean escalation to **1.23**, and restores fact-seeking inquiry to **100%**.

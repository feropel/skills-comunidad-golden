# Costos por motor y punto de equilibrio

<!-- Extraído de SKILL.md v1.14 (2026-09-05) para bajar el coste de activación. Fuente única: este archivo. -->

## Cost reality check (why we stay on Higgsfield)

Pay-per-use aggregators (self-hosted frontends over MuAPI-style gateways) look "free" because the
repo is free — **the generations are not**. Verified market prices (mayo 2026), useful both to pick
the right model per job and to sanity-check any "free alternative":

| Model | What it is | ~Cost per generation | Best for |
|---|---|---|---|
| Flux Schnell | fast image | ~$0.03 | iterating ideas |
| Flux Pro | pro image | ~$0.10 | final deliverables |
| Midjourney v7 | stylised image | ~$0.15 | brand/aesthetic shots |
| Kling 2.5 | ~5s realistic video | ~$0.50 | reels, product motion |
| Sora 2 | ~10s cinematic video | ~$2.00 | hero shots |
| Veo 3 | ~8s video with audio | ~$3.00 | ads with sound |

**The break-even that nobody does:** under ~30 generations/month, pay-per-use is cheaper (saves
~$19/mo). At ~60-100/month it is a tie. **Above ~200/month you pay 3-5x more** than a flat
subscription. Golden operates well above the tie point (UGC + product images + ads), so the
**Higgsfield subscription stays** — and any "install this free repo instead" claim gets checked
against this table before switching. Rule: iterate with the cheap model, spend on the final only.


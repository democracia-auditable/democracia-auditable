# Democracia Auditable

**Applying safety engineering to democratic oversight**  
*A proposal for an open protocol to reconstruct public decisions, verify warnings and document institutional responses.*

**Presentation document for independent evaluation · Based on v0.4.9 · 2 November 2026**  
**English translation of the presentation. The full working paper, the study and the repository are in Spanish.**

> Human beings are imperfect. Institutions should be designed so that our mistakes —and our possible abuses— do not turn into catastrophes, and so that well-founded warnings cannot be ignored without leaving a trace.

## The problem it seeks to address

A democracy has elections, parliaments, courts, oversight bodies and rights of access to information. Yet, for a specific public decision, it can be hard to reconstruct **what information existed, who detected a problem, whom it was reported to, what response it received and what happened next**. The proposal does not assume that institutions fail to meet their obligations: it puts forward a method to check how their mechanisms for detection, response and correction actually work.

## What is proposed

**A protocol for distributed and verifiable oversight**, inspired by safety-critical systems engineering: traceability, independent controls, defence in depth, error logging and learning from incidents. Its intended output is a record that third parties can reconstruct, not an automatic verdict or a new authority. An identifiable organisation would have to take legal and editorial responsibility for any real implementation.

## How the protocol would work

**1. Gather evidence.** Locate public sources and keep their origin, date, version and document fingerprint; distinguish facts on record, information not located and interpretations.

**2. Cross-check and verify.** Compare independent documents and methods, record discrepancies and submit what matters to human review. Keep quality of evidence, potential impact and urgency separate; never turn these axes into a score of people or institutions.

**3. Use the appropriate channel.** When documentation is missing or there is a well-founded warning, first determine which legal procedure applies. Record the recipient, date of receipt, legal basis, verified deadline and, where appropriate, the complaint or referral to the competent body.

**4. Leave a verifiable record.** Record responses, reasoned rejections, corrections and **the absence of any located response as of a given date**, without equating silence with guilt. Where it is lawful and prudent to publish it, allow a question already asked, and its outcome, to be reused.

**5. Audit the oversight itself.** Publish methods, errors, limitations, negative results and corrections; make room for rebuttal and external evaluation. If a tool —AI included— adds no value over a simpler alternative, it is dropped.

---

## What its implementation would aim to achieve

**That well-founded warnings are not lost along the way.** Being able to reconstruct what was reported, through which channel and what action is on record, without attributing intentions or requiring every warning to be accepted.

**That institutional response becomes measurable.** Counting admissible requests, reasoned responses and the legally applicable deadlines; distinguishing a gap in documentation, an error of the protocol itself and a genuinely proven breach.

**That knowledge accumulates.** Avoiding needlessly repeated questions and making documents, responses and corrections more accessible, within legal and privacy constraints.

**That oversight also serves those being overseen.** Detecting where data are missing, where workloads concentrate and what information would be worth publishing proactively. The goal is to fix operational failures, not to produce partisan rankings.

## A first application: how public works end

To put the idea to the test, work began with public works contracts. An automated analysis, **without artificial intelligence** (using fixed rules), examined open data from Spain's Public Sector Procurement Platform (Plataforma de Contratación del Sector Público, PLACSP). Among **1,593 tender files** for works awarded in 2023, with a base budget of €1–10 million excluding VAT and a theoretical completion date before the cut-off, **in 1,549 (97.2%) the program found no indicator of completion or termination in the fields examined**.

This figure **does not show that the works were not completed, that documents are missing through other channels or that any law was breached**. It points to a difficulty in locating information in one specific channel, and justifies checking it through a pilot. The project's operational annex proposes selection rules, a limited number of requests, a log of responses and deadline tracking, always with human verification.

## Safeguards and limits

The protocol **does not replace** judges, auditors, parliaments or competent authorities; it does not decide policy, accuse anyone of crimes or score people. It triggers no automatic sanctions or vetoes, and it is not an emergency channel. It requires privacy, a right of reply, visible corrections, independent editorial control and an assessment of the harm that the oversight itself might cause. AI is optional and must prove its advantage over manual or deterministic methods.

## Current status and availability

There is a **methodological draft**, a reproducible study and tools to prepare a pilot on public works. **No pilot with real requests has been carried out, and there is no legal, statistical or institutional validation by human specialists.** All reviews so far have been carried out with AI models, so their conclusions need independent checking.

This work is made available to anyone who finds it useful, as an **open proposal, not a closed protocol to be adopted in full**. Readers may examine it critically, question its assumptions, take only the principles, procedures or tools they find useful, adapt them to their own initiatives or discard the proposal.

Anyone who believes that the protocol, or part of it, deserves to be tested may do so under their own responsibility and with the corresponding technical and legal review. A small pilot would make it possible to measure results, costs and possible unintended effects.

**No endorsement, funding or ongoing commitment is requested.** The purpose is to share the work done so that anyone can freely judge whether it contains something useful to them. The project has no operating sponsor; the original texts are offered under CC0 and the code under MIT-0.

**Repository and full documentation (in Spanish):** https://github.com/democracia-auditable/democracia-auditable  
**To go further:** main paper, §§ 1–3, 5–7 and 9–10; study, § 9.0 bis; public works pilot, annex D.

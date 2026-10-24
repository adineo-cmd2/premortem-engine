"""Template scenario packs per project_type.

Each pack has 10 entries with distribution technicalx2, teamx2, marketx2,
executionx2, dependencyx1, unknownx1. Templates use {name} (project name),
{desc} (short description), {dep} (first dependency or fallback),
{team} (team size). LLM hook: template passthrough when no API keys set.
"""

import os

CATEGORIES = ("technical", "team", "market", "execution", "dependency", "unknown")

_FALLBACK_DEP = "a key dependency"


def _pack(
    cat1, title1, nar1, prob1, sev1, warn1, key1,
    cat2, title2, nar2, prob2, sev2, warn2, key2,
    cat3, title3, nar3, prob3, sev3, warn3, key3,
    cat4, title4, nar4, prob4, sev4, warn4, key4,
    cat5, title5, nar5, prob5, sev5, warn5, key5,
    cat6, title6, nar6, prob6, sev6, warn6, key6,
    cat7, title7, nar7, prob7, sev7, warn7, key7,
    cat8, title8, nar8, prob8, sev8, warn8, key8,
    cat9, title9, nar9, prob9, sev9, warn9, key9,
    cat10, title10, nar10, prob10, sev10, warn10, key10,
):
    rows = [
        (cat1, title1, nar1, prob1, sev1, warn1, key1),
        (cat2, title2, nar2, prob2, sev2, warn2, key2),
        (cat3, title3, nar3, prob3, sev3, warn3, key3),
        (cat4, title4, nar4, prob4, sev4, warn4, key4),
        (cat5, title5, nar5, prob5, sev5, warn5, key5),
        (cat6, title6, nar6, prob6, sev6, warn6, key6),
        (cat7, title7, nar7, prob7, sev7, warn7, key7),
        (cat8, title8, nar8, prob8, sev8, warn8, key8),
        (cat9, title9, nar9, prob9, sev9, warn9, key9),
        (cat10, title10, nar10, prob10, sev10, warn10, key10),
    ]
    return [
        {
            "category": c, "title_t": t, "narrative_t": n,
            "probability": p, "severity": s, "warnings": list(w),
            "precedent_key": k,
        }
        for c, t, n, p, s, w, k in rows
    ]


SCENARIO_PACKS = {
    "software": _pack(
        "technical", "Launch-day outage in {name}",
        "Six months after launch, {name} ({desc}) collapses under real traffic: an untested "
        "deploy path corrupts state, rollback fails, and the team of {team} spends a week "
        "replaying data. Dependency {dep} throttles at the worst hour.",
        "high", "critical",
        ["error-rate spike on dashboards", "queue depth growing without draining", "p99 latency climbing week over week"],
        "knight_capital",
        "technical", "Silent data corruption in {name}",
        "{name} quietly writes bad records for weeks: two services disagree on units and formats, "
        "nobody owns the contract, and {desc} becomes untrustworthy before anyone notices.",
        "medium", "critical",
        ["mismatched counts between services", "rising support tickets about wrong data", "exports that no longer reconcile"],
        "mars_orbiter",
        "team", "Key engineers quit {name} mid-build",
        "Two senior builders leave {name} within a month; all context for {desc} lived in their heads. "
        "The remaining team of {team} stalls, and schedule pressure silences quality concerns.",
        "medium", "high",
        ["overtime trend for the same people", "reviews mentioning burnout", "bus factor of one on critical paths"],
        "challenger",
        "team", "Secrecy hides bad news in {name}",
        "Nobody on {name} will say the demo is faked: status stays green while {desc} rots. "
        "Leadership learns the truth from a customer, not the team of {team}.",
        "low", "high",
        ["demos that never show live data", "engineers avoiding written updates", "whistleblower-style rumors in 1:1s"],
        "theranos",
        "market", "Nobody wants {name}",
        "{name} ships on time and lands flat: users never felt the pain {desc} solves, and {dep} "
        "already bundles a good-enough alternative. The team of {team} built before interviewing.",
        "high", "high",
        ["pilot users going quiet", "trial-to-paid conversion under 5%", "competitor bundled for free"],
        "google_glass",
        "market", "Launch collapses like a bad rollout in {name}",
        "{name} opens to a flood it cannot serve: onboarding breaks, {desc} gets one-star reviews, "
        "and the press narrative hardens before a fix ships.",
        "medium", "high",
        ["onboarding drop-off above 60%", "support backlog doubling weekly", "negative press quoting users"],
        "healthcare_gov",
        "execution", "Automation meltdown delays {name}",
        "{name} bets everything on a bespoke pipeline with no manual fallback; on go-live week it jams, "
        "{desc} halts, and the team of {team} rebuilds by hand under deadline.",
        "medium", "high",
        ["integration tests skipped for speed", "no manual fallback rehearsed", "single bespoke component with no owner"],
        "denver_bags",
        "execution", "Scope creep sinks {name}",
        "{name} never freezes scope: fire-safety-grade late defects surface in {desc}, the date slips "
        "twice, and budget overruns force cuts to {dep} integration.",
        "high", "medium",
        ["scope additions after freeze date", "audit findings left open", "contingency budget already spent"],
        "ber_airport",
        "dependency", "{dep} fails and takes {name} down",
        "{name} discovers {dep} is a single point of failure with no backup: when it floods, {desc} "
        "goes dark and there is no second supplier to call.",
        "medium", "critical",
        ["single supplier with no backup", "backup never tested under load", "contract SLA weaker than your promise"],
        "fukushima_backup",
        "unknown", "Freak incident wrecks {name} launch week",
        "A once-a-decade storm plus a viral pile-on hits {name} during its biggest week: {desc} cannot "
        "absorb the surge, crowd sentiment turns, and the team of {team} has no abort criteria.",
        "low", "medium",
        ["no worst-case capacity plan", "safety staffing at minimum", "no pre-agreed abort criteria"],
        "event_rain",
    ),
    "hardware": _pack(
        "technical", "Field failures recall {name}",
        "Units of {name} ({desc}) die in the field: a tolerance stack-up nobody tested at scale bricks "
        "devices, and the team of {team} faces a recall with {dep} parts already committed.",
        "high", "critical",
        ["rising RMA rate on early units", "test escapes on tolerance edges", "supplier batch variation ignored"],
        "knight_capital",
        "technical", "Unit mismatch breaks {name}",
        "Two vendors for {name} use different units; {desc} integrates both without a contract test and "
        "the first production run is scrap.",
        "medium", "critical",
        ["interface spec unsigned", "integration test waived", "vendor datasheets disagreeing"],
        "mars_orbiter",
        "team", "Safety warnings overruled on {name}",
        "Engineers flag a cold-temperature failure mode in {name}; schedule pressure overrules them and "
        "{desc} ships anyway with the team of {team} watching nervously.",
        "medium", "high",
        ["safety memo without response", "schedule moved up despite flags", "no independent no-go authority"],
        "challenger",
        "team", "Hardware truth hidden from founders of {name}",
        "Yield data for {name} is massaged upward for months; {desc} looks ready while lines actually fail. "
        "Founders learn the truth when {dep} rejects a shipment.",
        "low", "high",
        ["yield reports improving too smoothly", "no live line demos", "quality staff excluded from reviews"],
        "theranos",
        "market", "Buyers reject {name} on price and privacy",
        "{name} works in the lab but buyers balk: {desc} costs too much, feels creepy, and {dep} "
        "ecosystem support never arrives.",
        "high", "high",
        ["pilot buyers not reordering", "price objections in every call", "ecosystem partner going quiet"],
        "google_glass",
        "market", "Launch-day overload buries {name}",
        "{name} launches to hype it cannot fulfil: ordering breaks, {desc} reviews savage the wait, and "
        "resellers flip scarce units at triple price.",
        "medium", "high",
        ["preorder volume above capacity", "fulfilment partner missing SLAs", "resale prices spiking"],
        "healthcare_gov",
        "execution", "Factory automation jams {name}",
        "{name} bets the line on bespoke automation with no manual fallback; it jams at rate, {desc} "
        "misses the season, and the team of {team} hand-builds at a loss.",
        "medium", "high",
        ["line rate never sustained 8h", "no manual fallback cell", "single bespoke fixture"],
        "denver_bags",
        "execution", "{name} opens years late and over budget",
        "Certification defects stall {name}: each fix in {desc} uncovers two more, {dep} rework piles up, "
        "and the opening slips year after year.",
        "high", "medium",
        ["certification findings open", "rework outpacing new build", "contingency already consumed"],
        "ber_airport",
        "dependency", "{dep} outage halts {name} line",
        "One supplier ({dep}) is the only qualified source for {name}; when it floods, {desc} stops and "
        "no second source exists.",
        "medium", "critical",
        ["sole-source critical part", "supplier audit overdue", "no qualified second source"],
        "fukushima_backup",
        "unknown", "Extreme weather destroys {name} launch event",
        "A storm week plus a viral safety scare hits {name}: {desc} demo tents flood, crowds surge, and "
        "the team of {team} has no abort plan.",
        "low", "medium",
        ["outdoor plan with no cover", "crowd plan untested", "no weather abort criteria"],
        "event_rain",
    ),
    "research": _pack(
        "technical", "Pipeline bug invalidates {name} results",
        "A deploy-style config error silently corrupts the {name} analysis: {desc} results look great until "
        "a reviewer reruns with {dep} and nothing replicates.",
        "high", "critical",
        ["results too good to check", "pipeline without pinned configs", "rerun giving different numbers"],
        "knight_capital",
        "technical", "Unit error dooms {name} instrument",
        "Two labs feeding {name} use different units; {desc} fuses both streams and the headline finding "
        "is an artefact the team of {team} must retract.",
        "medium", "critical",
        ["merged data without unit checks", "instrument specs disagreeing", "no cross-lab validation"],
        "mars_orbiter",
        "team", "Dissent silenced on {name}",
        "Junior researchers doubt the {name} result but stay quiet; {desc} publishes, then collapses when "
        "a rival lab with fresh eyes reruns it.",
        "medium", "high",
        ["concerns raised only orally", "authorship tied to agreement", "no pre-registered analysis"],
        "challenger",
        "team", "Lab secrecy hides {name} failure",
        "The {name} protocol never quite works, but updates stay rosy; {desc} burns a year before {dep} "
        "collaborators see raw data.",
        "low", "high",
        ["raw data never shared", "protocols described vaguely", "replication requests deflected"],
        "theranos",
        "market", "Nobody funds {name} phase two",
        "{name} answers a question nobody will pay to solve: {desc} impresses reviewers but funders and "
        "{dep} partners walk away.",
        "high", "high",
        ["funders asking for applications", "partners not renewing", "citations without adoption"],
        "google_glass",
        "market", "Botched {name} launch poisons the well",
        "{name} launches its portal/cohort to fanfare and it crashes: {desc} headlines become the outage, "
        "and recruitment never recovers.",
        "medium", "high",
        ["pilot portal load untested", "support inbox overflowing", "press quoting angry users"],
        "healthcare_gov",
        "execution", "Over-automated {name} pipeline jams",
        "{name} automates collection end-to-end with no manual fallback; it jams mid-season, {desc} loses "
        "irreplaceable data, and the team of {team} hand-codes recovery.",
        "medium", "high",
        ["no manual collection fallback", "pipeline tested on toy data", "single bespoke instrument"],
        "denver_bags",
        "execution", "{name} slips years over budget",
        "Approvals and build-out for {name} compound: {desc} misses two field seasons, {dep} costs double, "
        "and funders lose patience.",
        "high", "medium",
        ["permits still pending", "field seasons missed", "budget contingency gone"],
        "ber_airport",
        "dependency", "{dep} loss kills {name} data",
        "The {name} archive lives on {dep} with no second copy; a flood-grade outage deletes months of "
        "{desc} work.",
        "medium", "critical",
        ["single archive copy", "backups never restore-tested", "vendor SLA weaker than grant terms"],
        "fukushima_backup",
        "unknown", "Freak conditions ruin {name} field season",
        "A record storm plus a local disruption wipes the {name} field window: {desc} has no backup site "
        "and the team of {team} flies home empty.",
        "low", "medium",
        ["single field site", "no backup season booked", "no abort/reschedule criteria"],
        "event_rain",
    ),
    "event": _pack(
        "technical", "Ticketing outage chaos at {name}",
        "Gates open for {name} ({desc}) and scanning dies: an untested deploy plus {dep} throttling strands "
        "thousands while the team of {team} reboots under pressure.",
        "high", "critical",
        ["scan failure in rehearsal", "vendor throttling at peak", "no offline ticket fallback"],
        "knight_capital",
        "technical", "Sound/light mismatch ruins {name}",
        "Two crews for {name} run different specs; {desc} opens with dead zones the team of {team} cannot "
        "patch mid-show.",
        "medium", "critical",
        ["rig plot unsigned", "soundcheck skipped", "crew specs disagreeing"],
        "mars_orbiter",
        "team", "Crew warnings ignored before {name}",
        "Riggers flag a structure risk for {name}; producers overrule them to protect the {desc} schedule "
        "and open the doors anyway.",
        "medium", "high",
        ["safety flag without response", "schedule overriding safety", "no independent show-stop authority"],
        "challenger",
        "team", "Headliner lies sink {name}",
        "Talent for {name} promises the moon while {desc} logistics rot; the team of {team} learns the "
        "truth when {dep} pulls out days before.",
        "low", "high",
        ["contracts unsigned late", "talent avoiding production calls", "rumors in vendor backchannels"],
        "theranos",
        "market", "Nobody buys tickets to {name}",
        "{name} guesses wrong on price and vibe: {desc} feels overpriced and off-trend while {dep} "
        "sponsors drift to a rival weekend.",
        "high", "high",
        ["presale under 30% of target", "sponsors downgrading", "social sentiment flat"],
        "google_glass",
        "market", "Gate crush overwhelms {name}",
        "{name} sells out but cannot ingress: {desc} queues explode, phones die, and the story becomes "
        "the chaos, not the show.",
        "medium", "high",
        ["ingress never load-tested", "security understaffed", "comms plan untested"],
        "healthcare_gov",
        "execution", "Logistics automation fails {name}",
        "The bespoke wristband/shuttle system for {name} jams on day one with no manual fallback; {desc} "
        "stalls while the team of {team} goes paper-based.",
        "medium", "high",
        ["vendor system never piloted", "no paper fallback printed", "single bespoke access system"],
        "denver_bags",
        "execution", "{name} venue slips years over budget",
        "Permits and build-out for {name} spiral: {desc} misses its announced year, costs double, and "
        "{dep} partners sue.",
        "high", "medium",
        ["permits still pending", "build costs doubling", "partners lawyering up"],
        "ber_airport",
        "dependency", "{dep} blackout darkens {name}",
        "The {name} site depends on {dep} power with no backup; a storm-grade outage kills cooling, "
        "lights, and {desc} mid-show.",
        "medium", "critical",
        ["single power feed", "generators never load-tested", "fuel contract unconfirmed"],
        "fukushima_backup",
        "unknown", "Storm and riot spiral at {name}",
        "Heat, rain, and short water turn {name} ({desc}) feral: crowds surge, the team of {team} has no "
        "abort criteria, and cameras roll.",
        "low", "medium",
        ["water plan at minimum", "no shade/cooling reserve", "no show-cancel criteria"],
        "event_rain",
    ),
    "business": _pack(
        "technical", "Billing outage torches {name} revenue",
        "On the biggest sales week, {name} ({desc}) double-charges and locks accounts: an untested deploy "
        "plus {dep} throttling burns trust the team of {team} cannot buy back.",
        "high", "critical",
        ["chargeback rate climbing", "billing deploys without rehearsal", "support macros for billing spiking"],
        "knight_capital",
        "technical", "Reporting units lie to {name} leadership",
        "Two systems feed {name} numbers in different units; {desc} decisions run on fiction for a quarter "
        "before finance catches it.",
        "medium", "critical",
        ["dashboards disagreeing", "manual spreadsheet fixes", "no metric definitions owned"],
        "mars_orbiter",
        "team", "Schedule pressure silences {name} staff",
        "Operators warn the {name} launch is unsafe; leadership ships {desc} anyway and the team of "
        "{team} learns to stay quiet.",
        "medium", "high",
        ["safety flags without response", "dates moved up arbitrarily", "no anonymous feedback channel"],
        "challenger",
        "team", "Cooked metrics hide {name} rot",
        "{name} reports growth while {desc} churns underneath; the board learns from {dep} partners, not "
        "the team of {team}.",
        "low", "high",
        ["metrics improving too smoothly", "churn buried in footnotes", "audits deflected"],
        "theranos",
        "market", "Market rejects {name} pricing",
        "{name} launches {desc} at a price nobody pays while {dep} bundles good-enough free; pipeline "
        "evaporates in a quarter.",
        "high", "high",
        ["discounts widening to close", "free competitor bundled", "pilots not converting"],
        "google_glass",
        "market", "Botched {name} launch burns the brand",
        "{name} opens {desc} to demand it cannot serve; onboarding breaks, reviews tank, and recovery "
        "costs more than the launch made.",
        "medium", "high",
        ["onboarding failing at volume", "review scores dropping", "refund rate climbing"],
        "healthcare_gov",
        "execution", "Fulfilment meltdown misses {name} season",
        "{name} bets fulfilment on one bespoke flow with no manual fallback; peak week jams, {desc} "
        "misses Christmas, and the team of {team} refunds en masse.",
        "medium", "high",
        ["peak simulation never run", "no manual packing fallback", "single 3PL with no backup"],
        "denver_bags",
        "execution", "{name} expansion runs years over budget",
        "The {name} build-out never freezes scope: {desc} costs double, opens late, and {dep} leases "
        "bleed cash meanwhile.",
        "high", "medium",
        ["scope growing after freeze", "contractor claims rising", "contingency spent early"],
        "ber_airport",
        "dependency", "{dep} collapse strands {name}",
        "{name} single-sources {dep}; when the supplier floods, {desc} stops shipping and customers flee "
        "before a second source qualifies.",
        "medium", "critical",
        ["sole supplier critical input", "no dual-sourcing plan", "inventory below disruption cover"],
        "fukushima_backup",
        "unknown", "Black-swan week hits {name}",
        "A storm plus a viral boycott hits {name} together: {desc} stores flood, sentiment craters, and "
        "the team of {team} has no crisis playbook.",
        "low", "medium",
        ["no crisis playbook", "insurance gaps unreviewed", "no pre-agreed closure criteria"],
        "event_rain",
    ),
    "general": _pack(
        "technical", "Systems outage cripples {name}",
        "At the worst moment, {name} ({desc}) goes down: an untested change plus {dep} throttling breaks "
        "core flows and the team of {team} scrambles without a runbook.",
        "high", "critical",
        ["error budgets burning", "deploys without rehearsal", "alerts firing unanswered"],
        "knight_capital",
        "technical", "Misaligned parts break {name}",
        "Two halves of {name} were built to different specs; {desc} integrates them late and the team of "
        "{team} discovers nothing fits.",
        "medium", "critical",
        ["specs unsigned", "integration test waived", "vendors contradicting each other"],
        "mars_orbiter",
        "team", "Warnings ignored on {name}",
        "People staffing {name} flag the risk plainly; deadline pressure overrules them and {desc} "
        "proceeds toward a preventable failure.",
        "medium", "high",
        ["written warnings unanswered", "dates overriding safety", "no independent veto"],
        "challenger",
        "team", "Rosy reporting hides {name} trouble",
        "Status for {name} stays green while {desc} decays; leaders hear the truth from {dep} outsiders, "
        "not the team of {team}.",
        "low", "high",
        ["status always green", "bad news only verbal", "outsiders raising flags first"],
        "theranos",
        "market", "Nobody wants {name}",
        "{name} launches {desc} to indifference: the pain was assumed, {dep} already covers it, and "
        "adoption flatlines.",
        "high", "high",
        ["pilots going quiet", "adoption under target", "competitor bundled free"],
        "google_glass",
        "market", "Launch overload sinks {name}",
        "{name} meets demand it cannot serve: {desc} breaks at peak, reviews savage it, and trust never "
        "recovers.",
        "medium", "high",
        ["peak load untested", "support queues exploding", "press quoting failures"],
        "healthcare_gov",
        "execution", "Bespoke system jams {name}",
        "The custom backbone of {name} jams at go-live with no manual fallback; {desc} halts while the "
        "team of {team} rebuilds by hand.",
        "medium", "high",
        ["no fallback rehearsed", "single bespoke component", "integration tests skipped"],
        "denver_bags",
        "execution", "{name} runs late and over budget",
        "Scope for {name} never freezes: {desc} slips twice, costs double, and {dep} work must be cut to "
        "survive.",
        "high", "medium",
        ["scope growing", "audits open", "contingency spent"],
        "ber_airport",
        "dependency", "{dep} failure stops {name}",
        "{name} leans wholly on {dep}; when it fails, {desc} stops and there is no backup to switch to.",
        "medium", "critical",
        ["single point of failure", "backup never tested", "SLA weaker than promise"],
        "fukushima_backup",
        "unknown", "Freak week derails {name}",
        "Storm, surge, and sentiment hit {name} at once: {desc} cannot absorb it and the team of {team} "
        "has no abort criteria.",
        "low", "medium",
        ["no worst-case plan", "reserves at minimum", "no abort criteria"],
        "event_rain",
    ),
}

# Spec §2 names the fallback pack "default"; keep both spellings.
SCENARIO_PACKS["default"] = SCENARIO_PACKS["general"]


def _llm_keys_present() -> bool:
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY"))


def generate(name, description, ptype, team_size, deps):
    """Build 10 scenario dicts from the template pack.

    LLM hook: when no API keys are set this is a pure template passthrough.
    When keys are present, a future LLM pass may rewrite title/narrative;
    templates are still the fallback. Returns list of dicts with keys
    category, title, narrative, probability, severity, precedent_key, warnings.
    """
    pack = SCENARIO_PACKS.get((ptype or "").lower(), SCENARIO_PACKS["general"])
    pname = (name or "").strip() or "Untitled project"
    desc_full = (description or "").strip() or "a new venture"
    desc = desc_full[:120]
    dep = (deps[0] if deps else None) or _FALLBACK_DEP
    team = str(team_size if team_size else "a small")

    scenarios = []
    for entry in pack:
        scenarios.append({
            "category": entry["category"],
            "title": entry["title_t"].format(name=pname, desc=desc, dep=dep, team=team),
            "narrative": entry["narrative_t"].format(name=pname, desc=desc, dep=dep, team=team),
            "probability": entry["probability"],
            "severity": entry["severity"],
            "precedent_key": entry["precedent_key"],
            "warnings": list(entry["warnings"]),
        })

    # LLM enhancement hook (same pattern as sibling engines): only when keys
    # exist; otherwise return templates unchanged.
    if _llm_keys_present():
        scenarios = _maybe_enhance_with_llm(scenarios, pname, desc_full)
    return scenarios


def _maybe_enhance_with_llm(scenarios, name, description):
    """Placeholder LLM rewrite. Returns template scenarios unchanged so the
    engine works with or without keys (mock-first, self-contained)."""
    return scenarios

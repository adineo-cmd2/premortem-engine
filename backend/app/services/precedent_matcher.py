"""Real historical failure precedents. Every record is a famous verifiable
failure with a cited year. Used by scenario_generator packs via precedent_key."""

REAL_PRECEDENTS = {
    "knight_capital": {
        "project_name": "Knight Capital",
        "year": 2012,
        "industry": "finance",
        "what_happened": (
            "A dead trading flag reactivated on deploy sent millions of bad "
            "orders; Knight lost ~$440M in under an hour."
        ),
        "prevention": "Staged deploys, feature flags, automated kill switch, deploy rehearsal.",
    },
    "healthcare_gov": {
        "project_name": "Healthcare.gov",
        "year": 2013,
        "industry": "software",
        "what_happened": (
            "The US health-exchange launch crashed under load after weak "
            "end-to-end testing and tangled contractor ownership."
        ),
        "prevention": "Load-test at 10x forecast, single accountable integrator, phased rollout.",
    },
    "challenger": {
        "project_name": "Challenger shuttle",
        "year": 1986,
        "industry": "aerospace",
        "what_happened": (
            "O-ring failure destroyed the shuttle; engineers' cold-weather "
            "warnings were overruled by schedule pressure."
        ),
        "prevention": "Independent safety veto, anonymous dissent channel, no-go authority for engineers.",
    },
    "denver_bags": {
        "project_name": "Denver airport baggage",
        "year": 1995,
        "industry": "software",
        "what_happened": (
            "Denver airport's automated baggage system jammed and mauled "
            "luggage, delaying the airport opening by 16 months."
        ),
        "prevention": "De-scope automation, manual fallback from day one, phased terminal rollout.",
    },
    "ber_airport": {
        "project_name": "Berlin BER airport",
        "year": 2012,
        "industry": "construction",
        "what_happened": (
            "Berlin's new airport missed its 2012 opening over fire-safety and "
            "systems defects, opening 9 years late and billions over budget."
        ),
        "prevention": "Freeze scope early, independent systems audit, realistic contingency buffers.",
    },
    "mars_orbiter": {
        "project_name": "Mars Climate Orbiter",
        "year": 1999,
        "industry": "aerospace",
        "what_happened": (
            "A metric/imperial unit mismatch between teams sent the orbiter "
            "into Mars' atmosphere, destroying a $125M mission."
        ),
        "prevention": "Contract-level interface specs, cross-team integration tests, unit-check linting.",
    },
    "theranos": {
        "project_name": "Theranos",
        "year": 2015,
        "industry": "health",
        "what_happened": (
            "Secretive culture hid that the blood-testing devices did not "
            "work; whistleblowers were silenced until collapse and prosecution."
        ),
        "prevention": "Independent validation, protected whistleblowing, demo-or-it-didn't-happen reviews.",
    },
    "fukushima_backup": {
        "project_name": "Fukushima backup power",
        "year": 2011,
        "industry": "energy",
        "what_happened": (
            "The tsunami flooded backup generators sited too low, knocking "
            "out cooling and causing triple meltdown."
        ),
        "prevention": "Map single points of failure, second supplier, backup for the backup.",
    },
    "google_glass": {
        "project_name": "Google Glass",
        "year": 2013,
        "industry": "hardware",
        "what_happened": (
            "A technically working product flopped as the public rejected "
            "camera-glasses on privacy and price grounds."
        ),
        "prevention": "Problem interviews before building, pricing tests, small public pilot first.",
    },
    "event_rain": {
        "project_name": "Woodstock 99",
        "year": 1999,
        "industry": "events",
        "what_happened": (
            "Under-provisioned water, shade, and crowd control turned a "
            "festival into riots and fires on live TV."
        ),
        "prevention": "Capacity-plan for worst weather, over-provision water/safety, abort criteria set in advance.",
    },
}


def match(key: str) -> dict:
    """Return a copy of the precedent record for key. Raises KeyError if unknown."""
    rec = REAL_PRECEDENTS[key]
    return dict(rec)

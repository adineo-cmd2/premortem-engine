import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../lib/apiClient';
const BASE = (import.meta.env.BASE_URL ?? '/').replace(/\/$/, '');

interface PrecedentRecord {
  project_name?: string;
  year?: number;
  industry?: string;
  what_happened?: string;
  prevention?: string;
}

interface Scenario {
  id: number;
  category: string;
  title: string;
  narrative: string;
  probability: string;
  severity: string;
  precedent?: string;
  precedent_record?: PrecedentRecord | null;
  precedent_detail?: PrecedentRecord | null;
  warnings: string[];
}

function precedentOf(s: Scenario): PrecedentRecord | null {
  return s.precedent_record ?? s.precedent_detail ?? null;
}

function sevStyle(sev: string): string {
  if (sev === 'critical') return 'border-riskred/60 bg-red-50 text-riskred';
  if (sev === 'high') return 'border-riskamber/60 bg-amber-50 text-riskamber';
  return 'border-riskblue/60 bg-blue-50 text-riskblue';
}

export default function ScenarioList({ sid }: { sid: string }) {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [err, setErr] = useState<string>('');
  const [info, setInfo] = useState<string>('');
  const [catFilter, setCatFilter] = useState<string>('all');
  const [sevFilter, setSevFilter] = useState<string>('all');
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});
  const [selected, setSelected] = useState<Record<number, boolean>>({});
  const [busy, setBusy] = useState<boolean>(false);

  useEffect(() => {
    if (!sid) return;
    apiGet(`/api/premortem/${sid}/scenarios`)
      .then((d) => {
        const list: Scenario[] = Array.isArray(d) ? d : (d?.scenarios ?? []);
        setScenarios(list);
      })
      .catch((e) => setErr(e instanceof Error ? e.message : 'Scenarios load failed.'));
  }, [sid]);

  if (!sid) return <p className="text-xs text-charcoal/70">No session selected.</p>;
  if (err) return <p className="text-sm text-riskred">{err}</p>;
  if (!scenarios.length) return <p className="text-sm text-charcoal/70">Loading scenarios…</p>;

  const categories = Array.from(new Set(scenarios.map((s) => s.category)));
  const filtered = scenarios.filter(
    (s) =>
      (catFilter === 'all' || s.category === catFilter) &&
      (sevFilter === 'all' || s.severity === sevFilter),
  );

  function toggleExpand(id: number) {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  function toggleSelect(id: number) {
    setSelected((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  const selectedIds = Object.entries(selected)
    .filter(([, v]) => v)
    .map(([k]) => Number(k));

  async function planMitigations() {
    setInfo('');
    setErr('');
    if (!selectedIds.length) {
      setErr('Select at least one scenario to plan mitigations.');
      return;
    }
    setBusy(true);
    try {
      // Defensive: backend may return a flat array OR {mitigations}.
      const d = await apiPost(`/api/premortem/${sid}/mitigate`, {
        scenario_ids: selectedIds,
      });
      const count = Array.isArray(d) ? d.length : (d?.mitigations?.length ?? selectedIds.length);
      setInfo(`Planned mitigations for ${selectedIds.length} scenario(s) (${count} actions).`);
      if (typeof window !== 'undefined') {
        window.location.href = `${BASE}/mitigations?sid=${sid}`;
      }
    } catch (e) {
      setErr(e instanceof Error ? e.message : 'Mitigate failed.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-2 text-sm">
        <label className="text-xs font-bold text-boardroom">
          Category{' '}
          <select
            value={catFilter}
            onChange={(e) => setCatFilter(e.target.value)}
            className="ml-1 rounded border border-boardroom/30 bg-white p-1 text-xs"
          >
            <option value="all">all</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        <label className="text-xs font-bold text-boardroom">
          Severity{' '}
          <select
            value={sevFilter}
            onChange={(e) => setSevFilter(e.target.value)}
            className="ml-1 rounded border border-boardroom/30 bg-white p-1 text-xs"
          >
            <option value="all">all</option>
            <option value="critical">critical</option>
            <option value="high">high</option>
            <option value="medium">medium</option>
          </select>
        </label>
        <button
          type="button"
          onClick={planMitigations}
          disabled={busy || !selectedIds.length}
          className="ml-auto rounded bg-boardroom px-3 py-1.5 text-xs font-bold text-white disabled:opacity-50"
        >
          {busy ? 'Planning…' : `Plan mitigations (${selectedIds.length})`}
        </button>
      </div>
      {info && <p className="mb-2 text-xs text-riskblue">{info}</p>}
      <ul className="space-y-2">
        {filtered.map((s) => {
          const prec = precedentOf(s);
          const open = !!expanded[s.id];
          return (
            <li key={s.id} className="rounded border border-boardroom/20 bg-white p-3 text-sm">
              <div className="flex flex-wrap items-center gap-2">
                <input
                  type="checkbox"
                  checked={!!selected[s.id]}
                  onChange={() => toggleSelect(s.id)}
                  aria-label={`Plan mitigation for scenario ${s.id}`}
                />
                <span className="rounded bg-boardroom px-1.5 py-0.5 text-xs text-white">{s.category}</span>
                <span className={`rounded border px-1.5 py-0.5 text-xs ${sevStyle(s.severity)}`}>
                  {s.severity} / {s.probability}
                </span>
                <button
                  type="button"
                  onClick={() => toggleExpand(s.id)}
                  className="text-left font-semibold text-boardroom hover:underline"
                >
                  {s.title}
                </button>
              </div>
              {open && (
                <div className="mt-2 space-y-2 text-xs text-charcoal">
                  <p>{s.narrative}</p>
                  {(s.precedent || prec) && (
                    <p className="rounded bg-slate-100 p-2">
                      <strong>Precedent:</strong> {s.precedent}
                      {prec?.project_name && (
                        <span>
                          {' '}
                          — {prec.project_name}
                          {prec.year ? ` (${prec.year})` : ''}
                          {prec.what_happened ? `: ${prec.what_happened}` : ''}
                          {prec.prevention ? ` Lesson: ${prec.prevention}` : ''}
                        </span>
                      )}
                    </p>
                  )}
                  {!!s.warnings?.length && (
                    <ul className="list-disc pl-5">
                      {s.warnings.map((w, i) => (
                        <li key={i}>{w}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </li>
          );
        })}
      </ul>
      {!filtered.length && <p className="mt-2 text-xs text-charcoal/70">No scenarios match filters.</p>}
    </div>
  );
}

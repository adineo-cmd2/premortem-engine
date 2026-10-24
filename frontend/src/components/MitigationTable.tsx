import { useEffect, useState } from 'react';
import { apiGet } from '../lib/apiClient';

interface Mitigation {
  id?: number;
  action: string;
  owner_role?: string;
  owner?: string;
  effort?: string;
  timeline_weeks?: number;
  weeks?: number;
}

interface Group {
  scenario_id: number;
  title?: string;
  category?: string;
  mitigations: Mitigation[];
}

function groupsOf(d: unknown): Group[] {
  if (Array.isArray(d)) {
    // Defensive: flat mitigation list — group by scenario_id client-side.
    const flat = d as Array<Mitigation & { scenario_id?: number; scenario_title?: string }>;
    const map = new Map<number, Group>();
    for (const m of flat) {
      const sid = m.scenario_id ?? 0;
      if (!map.has(sid)) map.set(sid, { scenario_id: sid, title: m.scenario_title ?? '', mitigations: [] });
      map.get(sid)!.mitigations.push(m);
    }
    return [...map.values()];
  }
  if (d && typeof d === 'object') {
    const obj = d as Record<string, unknown>;
    if (Array.isArray(obj.groups)) return obj.groups as Group[];
    if (Array.isArray(obj.mitigations)) return groupsOf(obj.mitigations);
  }
  return [];
}

function ownerOf(m: Mitigation): string {
  return m.owner_role ?? m.owner ?? '';
}

function weeksOf(m: Mitigation): string {
  const w = m.timeline_weeks ?? m.weeks;
  return w === undefined ? '' : String(w);
}

export default function MitigationTable({ sid }: { sid: string }) {
  const [groups, setGroups] = useState<Group[]>([]);
  const [err, setErr] = useState<string>('');

  useEffect(() => {
    if (!sid) return;
    apiGet(`/api/premortem/${sid}/mitigations`)
      .then((d) => setGroups(groupsOf(d)))
      .catch((e) => setErr(e instanceof Error ? e.message : 'Mitigations load failed.'));
  }, [sid]);

  if (!sid) return <p className="text-xs text-charcoal/70">No session selected.</p>;
  if (err) return <p className="text-sm text-riskred">{err}</p>;
  if (!groups.length) return <p className="text-sm text-charcoal/70">Loading mitigations… (run Plan mitigations from Scenarios first)</p>;

  function exportCsv() {
    const rows = [['scenario_id', 'scenario', 'category', 'action', 'owner', 'effort', 'weeks']];
    for (const g of groups) {
      for (const m of g.mitigations) {
        rows.push([
          String(g.scenario_id),
          `"${(g.title ?? '').replace(/"/g, '""')}"`,
          g.category ?? '',
          `"${m.action.replace(/"/g, '""')}"`,
          ownerOf(m),
          m.effort ?? '',
          weeksOf(m),
        ]);
      }
    }
    const csv = rows.map((r) => r.join(',')).join('\n');
    if (typeof window === 'undefined') return;
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `premortem-${sid}-mitigations.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div>
      <div className="mb-3 flex justify-end">
        <button
          type="button"
          onClick={exportCsv}
          className="rounded border border-boardroom/40 px-3 py-1.5 text-xs font-bold text-boardroom"
        >
          Export CSV
        </button>
      </div>
      {groups.map((g) => (
        <div key={g.scenario_id} className="mb-4 rounded border border-boardroom/20 bg-white">
          <div className="border-b border-boardroom/10 bg-slate-100 px-3 py-2 text-sm font-bold text-boardroom">
            #{g.scenario_id} {g.title ?? ''}{' '}
            {g.category && <span className="ml-1 text-xs font-normal text-charcoal/70">({g.category})</span>}
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-boardroom text-white">
                <tr>
                  <th className="px-3 py-2">Action</th>
                  <th className="px-3 py-2">Owner</th>
                  <th className="px-3 py-2">Effort</th>
                  <th className="px-3 py-2">Weeks</th>
                </tr>
              </thead>
              <tbody>
                {g.mitigations.map((m, i) => (
                  <tr key={m.id ?? i} className={i % 2 ? 'bg-slate-50' : 'bg-white'}>
                    <td className="px-3 py-2">{m.action}</td>
                    <td className="px-3 py-2">{ownerOf(m)}</td>
                    <td className="px-3 py-2">{m.effort ?? ''}</td>
                    <td className="px-3 py-2">{weeksOf(m)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}

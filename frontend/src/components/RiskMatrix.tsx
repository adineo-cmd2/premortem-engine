import { useEffect, useState } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
} from 'recharts';
import { apiGet } from '../lib/apiClient';

interface MatrixPoint {
  x: number;
  y: number;
  scenario: number;
  scenario_id?: number;
  title: string;
  category: string;
  severity?: string;
  probability?: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  technical: '#2563eb',
  team: '#d97706',
  market: '#dc2626',
  execution: '#0f766e',
  dependency: '#7c3aed',
  unknown: '#64748b',
};

function colorFor(category: string): string {
  return CATEGORY_COLORS[category] ?? '#0f172a';
}

export default function RiskMatrix({ sid }: { sid: string }) {
  const [points, setPoints] = useState<MatrixPoint[]>([]);
  const [err, setErr] = useState<string>('');

  useEffect(() => {
    if (!sid) return;
    apiGet(`/api/premortem/${sid}/risk-matrix`)
      .then((d) => {
        setPoints(Array.isArray(d?.points) ? d.points : []);
      })
      .catch((e) => setErr(e instanceof Error ? e.message : 'Matrix load failed.'));
  }, [sid]);

  if (!sid) return <p className="text-xs text-charcoal/70">No session selected.</p>;
  if (err) return <p className="text-sm text-riskred">{err}</p>;
  if (!points.length) return <p className="text-sm text-charcoal/70">Loading risk matrix…</p>;

  const grouped: Record<string, MatrixPoint[]> = {};
  for (const p of points) {
    const c = p.category || 'unknown';
    if (!grouped[c]) grouped[c] = [];
    grouped[c].push(p);
  }

  return (
    <div>
      <ResponsiveContainer width="100%" height={320}>
        <ScatterChart margin={{ top: 16, right: 16, bottom: 16, left: 0 }}>
          <CartesianGrid />
          <XAxis
            type="number"
            dataKey="x"
            domain={[0.5, 3.5]}
            ticks={[1, 2, 3]}
            tickFormatter={(v: number) => (v === 1 ? 'medium' : v === 2 ? 'high' : 'critical')}
            label={{ value: 'severity →', position: 'insideBottomRight', offset: -4, fontSize: 11 }}
          />
          <YAxis
            type="number"
            dataKey="y"
            domain={[0.5, 3.5]}
            ticks={[1, 2, 3]}
            tickFormatter={(v: number) => (v === 1 ? 'low' : v === 2 ? 'medium' : 'high')}
            label={{ value: 'probability', angle: -90, position: 'insideLeft', fontSize: 11 }}
          />
          <ZAxis type="number" range={[90, 90]} />
          <Tooltip
            formatter={(_v: unknown, _n: unknown, entry: any) => {
              const p = entry?.payload as MatrixPoint;
              return [`${p?.title ?? ''} (${p?.category ?? ''})`, `sev ${p?.x} / prob ${p?.y}`];
            }}
          />
          {Object.entries(grouped).map(([cat, pts]) => (
            <Scatter key={cat} name={cat} data={pts} fill={colorFor(cat)} />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
      <div className="mt-2 flex flex-wrap gap-2 text-xs">
        {Object.entries(grouped).map(([cat]) => (
          <span key={cat} className="rounded border border-boardroom/20 bg-white px-2 py-0.5">
            <span
              className="mr-1 inline-block h-2 w-2 rounded-full"
              style={{ backgroundColor: colorFor(cat) }}
            />
            {cat}
          </span>
        ))}
      </div>
    </div>
  );
}

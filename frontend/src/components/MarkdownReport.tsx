import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { apiGet } from '../lib/apiClient';

export default function MarkdownReport({ sid }: { sid: string }) {
  const [markdown, setMarkdown] = useState<string>('');
  const [err, setErr] = useState<string>('');
  const [copied, setCopied] = useState<boolean>(false);
  const [mdAvailable] = useState<boolean>(() => {
    try {
      return typeof ReactMarkdown !== 'undefined' && ReactMarkdown !== null;
    } catch {
      return false;
    }
  });

  useEffect(() => {
    if (!sid) return;
    apiGet(`/api/premortem/${sid}/report`)
      .then((d) => {
        setMarkdown(typeof d?.markdown === 'string' ? d.markdown : typeof d === 'string' ? d : '');
      })
      .catch((e) => setErr(e instanceof Error ? e.message : 'Report load failed.'));
  }, [sid]);

  if (!sid) return <p className="text-xs text-charcoal/70">No session selected.</p>;
  if (err) return <p className="text-sm text-riskred">{err}</p>;
  if (!markdown) return <p className="text-sm text-charcoal/70">Loading report…</p>;

  async function copy() {
    try {
      await navigator.clipboard.writeText(markdown);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  }

  function download() {
    if (typeof window === 'undefined') return;
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `premortem-${sid}-report.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div>
      <div className="mb-3 flex gap-2">
        <button
          type="button"
          onClick={copy}
          className="rounded bg-boardroom px-3 py-1.5 text-xs font-bold text-white"
        >
          {copied ? 'Copied!' : 'Copy'}
        </button>
        <button
          type="button"
          onClick={download}
          className="rounded border border-boardroom/40 px-3 py-1.5 text-xs font-bold text-boardroom"
        >
          Download .md
        </button>
      </div>
      <div className="rounded border border-boardroom/20 bg-white p-4">
        {mdAvailable ? (
          <div className="max-w-none text-sm">
            <ReactMarkdown>{markdown}</ReactMarkdown>
          </div>
        ) : (
          <pre className="whitespace-pre-wrap text-xs text-charcoal">{markdown}</pre>
        )}
      </div>
    </div>
  );
}

import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useId, useRef, useState } from "react";
import { Checkbox } from "@/components/ui/radix-checkbox";
import { Waves } from "@/components/ui/wave-background";
import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";
import { Terminal, ShieldAlert } from "lucide-react";
import { JollySelect, SelectItem } from "@/components/ui/select-1";
import { BlurFade } from "@/components/ui/blur-fade";
import { cn } from "@/lib/utils";
import TextMarquee from "@/components/ui/text-marque";

export const Route = createFileRoute("/")({
  component: Index,
});

const POS_OPTIONS = [
  "Marg ERP 9+",
  "TallyPrime",
  "Busy Accounting",
  "Vyapar",
  "Zoho Inventory",
  "Hitech BillSoft",
];

const DEBLOAT_LEVELS = ["Aggressive", "Basic", "None"] as const;

function Index() {
  const [debloat, setDebloat] = useState<(typeof DEBLOAT_LEVELS)[number]>("Basic");
  const [pos, setPos] = useState(POS_OPTIONS[0]);
  const [optimize, setOptimize] = useState(true);
  const [acknowledged, setAcknowledged] = useState(false);
  const [forging, setForging] = useState(false);
  const [logs, setLogs] = useState<string>(
    "[ READY ] Retail OS Forge terminal initialized.\n[ INFO ] Awaiting payload configuration...\n"
  );
  const termRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (termRef.current) termRef.current.scrollTop = termRef.current.scrollHeight;
  }, [logs]);

  const append = (text: string) => setLogs((p) => p + text);

  const handleForge = async () => {
    setForging(true);
    setLogs("");
    append(`[ ${new Date().toISOString()} ] INITIALIZING PAYLOAD...\n`);
    append(`[ CONFIG ] debloat_level=${debloat} | pos_software=${pos} | optimize_hardware=${optimize}\n\n`);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/forge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          debloat_level: debloat,
          pos_software: pos,
          optimize_hardware: optimize,
        }),
      });
      if (!res.ok || !res.body) throw new Error(`Engine responded ${res.status}`);
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        append(decoder.decode(value, { stream: true }));
      }
      append("\n[ COMPLETE ] Forge sequence finished.\n");
    } catch (err: any) {
      append(`\n[ ERROR ] ${err?.message ?? "Connection to local engine failed."}\n`);
      append("[ HINT  ] Ensure the Python engine is running at http://127.0.0.1:8000\n");
    } finally {
      setForging(false);
    }
  };

  return (
    <div className="dark relative min-h-screen w-full overflow-x-hidden text-foreground">
      <Waves className="pointer-events-none fixed inset-0 -z-10 h-screen w-screen" strokeColor="rgba(255,255,255,0.18)" backgroundColor="#000000" />
      <div className="pointer-events-none fixed inset-0 -z-10 bg-gradient-to-b from-black/40 via-transparent to-black/60" />

      {/* Big background marquee text */}
      <div className="pointer-events-none fixed inset-x-0 top-1/2 -z-10 -translate-y-1/2 select-none">
        <TextMarquee
          baseVelocity={-3}
          className="text-[18vw] font-black uppercase leading-none tracking-tighter text-white/[0.06] [text-shadow:_0_0_40px_rgba(255,255,255,0.05)]"
        >
          RETAIL OS FORGE
        </TextMarquee>
      </div>

      <main className="flex min-h-screen justify-center px-4 py-16">
        <div className="w-full max-w-3xl p-2 md:p-8">
          {/* Header */}
          <div className="mb-10 pb-6 text-center">
            <BlurFade delay={0.1} yOffset={10} blur="10px">
              <h1 className="bg-gradient-to-b from-white via-white to-white/40 bg-clip-text text-5xl font-black tracking-[0.2em] text-transparent drop-shadow-[0_0_30px_rgba(200,29,37,0.5)] md:text-7xl">
                RETAIL OS FORGE
              </h1>
            </BlurFade>
            <BlurFade delay={0.35} yOffset={6}>
              <p className="mt-4 text-xs uppercase tracking-[0.5em] text-white/60">
                Hardware Provisioning Payload
              </p>
            </BlurFade>
          </div>

          {/* Debloat */}
          <Section title="01 / Debloat Level">
            <div className="flex flex-wrap items-center justify-center gap-3">
              {DEBLOAT_LEVELS.map((lvl) => (
                <HoverBorderGradient
                  key={lvl}
                  as="button"
                  active={debloat === lvl}
                  onClick={() => setDebloat(lvl)}
                  className={cn(
                    "min-w-[140px] text-xs font-semibold uppercase tracking-[0.25em]",
                    debloat === lvl ? "text-white" : "text-white/60"
                  )}
                >
                  {lvl}
                </HoverBorderGradient>
              ))}
            </div>
          </Section>

          {/* POS Software */}
          <Section title="02 / POS Software">
            <JollySelect
              selectedKey={pos}
              onSelectionChange={(k) => setPos(String(k))}
              aria-label="POS Software"
            >
              {POS_OPTIONS.map((p) => (
                <SelectItem key={p} id={p}>
                  {p}
                </SelectItem>
              ))}
            </JollySelect>
          </Section>

          {/* Optimize */}
          <Section title="03 / Optimizations">
            <CheckboxRow
              checked={optimize}
              onChange={setOptimize}
              label="Optimize Files & Hardware (Disable Sleep, Telemetry, Copilot)"
            />
          </Section>

          {/* Legal */}
          <Section title="04 / Legal Acknowledgement">
            <div className="flex items-start gap-3 rounded-md border border-amber-500/20 bg-amber-500/5 p-4">
              <ShieldAlert className="mt-0.5 h-5 w-5 shrink-0 text-amber-400" />
              <CheckboxRow
                checked={acknowledged}
                onChange={setAcknowledged}
                label="I acknowledge this payload will alter system settings and install software. Creators are not liable for data loss."
              />
            </div>
          </Section>

          {/* Action */}
          <div className="mt-8 flex justify-center">
            <HoverBorderGradient
              as="button"
              disabled={!acknowledged || forging}
              onClick={handleForge}
              className="px-8 py-4 text-sm font-bold uppercase tracking-[0.3em]"
            >
              {forging ? "INITIALIZING PAYLOAD..." : "FORGE RETAIL TERMINAL"}
            </HoverBorderGradient>
          </div>

          {/* Terminal */}
          <div className="mt-8">
            <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-white/40">
              <Terminal className="h-3.5 w-3.5" />
              Live Terminal
            </div>
            <div
              ref={termRef}
              className="h-64 overflow-y-auto rounded-md border border-emerald-500/20 bg-black/90 p-4 font-mono text-xs leading-relaxed text-emerald-300 shadow-inner"
            >
              <pre className="whitespace-pre-wrap break-words">{logs}</pre>
              {forging && <span className="inline-block h-3 w-2 animate-pulse bg-emerald-400" />}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-6">
      <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.3em] text-white/40">
        {title}
      </div>
      {children}
    </div>
  );
}

function CheckboxRow({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (v: boolean) => void;
  label: string;
}) {
  const id = useId();
  return (
    <div className="flex items-start gap-3 text-sm text-white/80">
      <Checkbox
        id={id}
        checked={checked}
        onCheckedChange={(v) => onChange(Boolean(v))}
        className="mt-0.5 border border-white/30 bg-white/5 data-[state=checked]:bg-white data-[state=checked]:text-black"
      />
      <label htmlFor={id} className="cursor-pointer leading-relaxed">
        {label}
      </label>
    </div>
  );
}

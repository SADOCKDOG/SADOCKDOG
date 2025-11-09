"use client";

import * as React from "react";
import Link from "next/link";
import {
  useGetV2GetMyAgents,
} from "@/app/api/__generated__/endpoints/store/store";
import { usePostV1ExecuteGraphAgent } from "@/app/api/__generated__/endpoints/graphs/graphs";

// Simple, focused page to select one of "My Agents" and send a prompt to execute it.
// It leverages existing generated API hooks and keeps UX minimal and fast.

export default function SadockdogPage() {
  const { data: myAgentsResp, isLoading, error } = useGetV2GetMyAgents();
  const [selectedId, setSelectedId] = React.useState<string | null>(null);
  const [selectedVersion, setSelectedVersion] = React.useState<number | null>(
    null,
  );
  const [message, setMessage] = React.useState("");
  const [lastExecId, setLastExecId] = React.useState<string | null>(null);

  const { mutateAsync: executeGraph, isPending } = usePostV1ExecuteGraphAgent({
    mutation: {
      onSuccess: (res) => {
        const exec = res.data as any;
        const id = exec?.id ?? null;
        if (id) setLastExecId(id);
      },
    },
  });

  const agents = React.useMemo(() => {
    if (myAgentsResp?.status !== 200) return [] as Array<{
      id: string;
      version: number;
      name: string;
      description: string;
      image?: string | null;
      lastEdited: string;
    }>;
    return myAgentsResp.data.agents
      .map((a) => ({
        id: a.agent_id,
        version: a.agent_version,
        name: a.agent_name,
        description: a.description ?? "",
        image: a.agent_image ?? null,
        lastEdited: a.last_edited,
      }))
      .sort(
        (a, b) => new Date(b.lastEdited).getTime() - new Date(a.lastEdited).getTime(),
      );
  }, [myAgentsResp]);

  async function onRun() {
    if (!selectedId || selectedVersion == null || !message.trim()) return;
    await executeGraph({
      graphId: selectedId,
      graphVersion: selectedVersion,
      data: {
        inputs: { prompt: message },
        credentials_inputs: {},
      },
    });
  }

  return (
    <div className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-semibold">CHAT SADOCKDOG</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Selecciona uno de tus agentes y envíale una instrucción. Puedes abrir su
        vista completa para gestionar ejecuciones y ver el historial.
      </p>

      <div className="mt-6 grid gap-4">
        {isLoading && <div>Cargando tus agentes…</div>}
        {error && (
          <div className="text-red-600">
            Error cargando agentes. Asegúrate de haber iniciado sesión.
          </div>
        )}

        <div className="grid gap-2">
          <label className="text-sm font-medium">Agente</label>
          <select
            className="rounded-md border bg-background p-2"
            value={selectedId ?? ""}
            onChange={(e) => {
              const id = e.target.value || null;
              setSelectedId(id);
              const agent = agents.find((x) => x.id === id);
              setSelectedVersion(agent ? agent.version : null);
            }}
          >
            <option value="">— Selecciona un agente —</option>
            {agents.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name} (v{a.version})
              </option>
            ))}
          </select>
          {selectedId && (
            <div className="text-xs text-muted-foreground">
              Ver agente: {" "}
              <Link
                className="underline"
                href={`/platform/library/agents/${selectedId}`}
              >
                detalles y ejecuciones
              </Link>
            </div>
          )}
        </div>

        <div className="grid gap-2">
          <label className="text-sm font-medium">Mensaje</label>
          <textarea
            className="min-h-[100px] rounded-md border bg-background p-3"
            placeholder="Describe lo que quieres que haga el agente…"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>

        <div className="flex gap-2">
          <button
            className="rounded-md bg-primary px-4 py-2 text-primary-foreground disabled:opacity-50"
            disabled={!selectedId || !message.trim() || isPending}
            onClick={onRun}
          >
            {isPending ? "Ejecutando…" : "Ejecutar"}
          </button>
        </div>

        {lastExecId && selectedId && (
          <div className="rounded-md border bg-muted/30 p-3 text-sm">
            Ejecución iniciada: {lastExecId}. {" "}
            <Link
              className="underline"
              href={`/monitoring?executionId=${lastExecId}`}
            >
              Ver progreso
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

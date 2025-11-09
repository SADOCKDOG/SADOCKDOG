"use client";
import { Button } from "@/components/atoms/Button/Button";
import { useRouter } from "next/navigation";
import { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useToast } from "@/components/molecules/Toast/use-toast";
import { IconKey, IconUser } from "@/components/__legacy__/ui/icons";
import { Trash2Icon } from "lucide-react";
import { KeyIcon } from "@phosphor-icons/react/dist/ssr";
import { providerIcons } from "@/app/(platform)/library/agents/[id]/components/AgentRunsView/components/CredentialsInputs/CredentialsInputs";
import { CredentialsProvidersContext } from "@/providers/agent-credentials/credentials-provider";
import { getHiddenCredentialIds } from "@/lib/config/hiddenCredentials";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/__legacy__/ui/table";
import { CredentialsProviderName } from "@/lib/autogpt-server-api";
import { Dialog } from "@/components/molecules/Dialog/Dialog";
import { useSupabase } from "@/lib/supabase/hooks/useSupabase";
import LoadingBox from "@/components/__legacy__/ui/loading";

export default function UserIntegrationsPage() {
  const { supabase, user, isUserLoading } = useSupabase();
  const router = useRouter();
  const providers = useContext(CredentialsProvidersContext);
  const { toast } = useToast();

  const [confirmationDialogState, setConfirmationDialogState] = useState<
    | {
        open: true;
        message: string;
        onConfirm: () => void;
        onReject: () => void;
      }
    | { open: false }
  >({ open: false });

  const removeCredentials = useCallback(
    async (
      provider: CredentialsProviderName,
      id: string,
      force: boolean = false,
    ) => {
      if (!providers || !providers[provider]) {
        return;
      }

      let result;
      try {
        result = await providers[provider].deleteCredentials(id, force);
      } catch (error: any) {
        toast({
          title: "Something went wrong when deleting credentials: " + error,
          variant: "destructive",
          duration: 2000,
        });
        setConfirmationDialogState({ open: false });
        return;
      }
      if (result.deleted) {
        if (result.revoked) {
          toast({
            title: "Credentials deleted",
            duration: 2000,
          });
        } else {
          toast({
            title: "Credentials deleted from AutoGPT",
            description: `You may also manually remove the connection to AutoGPT at ${provider}!`,
            duration: 3000,
          });
        }
        setConfirmationDialogState({ open: false });
      } else if (result.need_confirmation) {
        setConfirmationDialogState({
          open: true,
          message: result.message,
          onConfirm: () => removeCredentials(provider, id, true),
          onReject: () => setConfirmationDialogState({ open: false }),
        });
      }
    },
    [providers, toast],
  );

  // System credentials that should be hidden from the UI
  // These are built-in "Use Credits for X" credentials
  // Configured via environment variables (see .env.example)
  const hiddenCredentials = useMemo(
    () => getHiddenCredentialIds(),
    [],
  );

  useEffect(() => {
    if (isUserLoading) return;
    if (!user || !supabase) router.push("/login");
  }, [isUserLoading, user, supabase, router]);

  if (isUserLoading) {
    return <LoadingBox className="h-[80vh]" />;
  }

  const allCredentials = providers
    ? Object.values(providers)
        .filter(
          (provider): provider is NonNullable<typeof provider> =>
            provider != null,
        )
        .flatMap((provider) =>
          provider.savedCredentials
            .filter(
              (cred) =>
                !hiddenCredentials.includes(cred.id) &&
                !cred.id.endsWith("-default"), // Hide SDK-registered default credentials
            )
            .map((credentials) => ({
              ...credentials,
              provider: provider.provider,
              providerName: provider.providerName,
              ProviderIcon: providerIcons[provider.provider] || KeyIcon,
              TypeIcon: {
                oauth2: IconUser,
                api_key: IconKey,
                user_password: IconKey,
                host_scoped: IconKey,
              }[credentials.type],
            })),
        )
    : [];

  return (
    <div className="mx-auto max-w-3xl md:py-8">
      <h2 className="mb-4 text-lg">Connections & Credentials</h2>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Provider</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {allCredentials.map((cred) => (
            <TableRow key={cred.id}>
              <TableCell>
                <div className="flex items-center space-x-1.5">
                  <cred.ProviderIcon className="h-4 w-4" />
                  <strong>{cred.providerName}</strong>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex h-full items-center space-x-1.5">
                  <cred.TypeIcon />
                  <span>{cred.title || cred.username}</span>
                </div>
                <small className="text-muted-foreground">
                  {
                    {
                      oauth2: "OAuth2 credentials",
                      api_key: "API key",
                      user_password: "Username & password",
                      host_scoped: "Host-scoped credentials",
                    }[cred.type]
                  }{" "}
                  - <code>{cred.id}</code>
                </small>
              </TableCell>
              <TableCell className="w-0 whitespace-nowrap">
                <Button
                  variant="destructive"
                  onClick={() => removeCredentials(cred.provider, cred.id)}
                >
                  <Trash2Icon className="mr-1.5 size-4" /> Delete
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Dialog
        controlled={{
          isOpen: confirmationDialogState.open,
          set: (open) => {
            if (!open) setConfirmationDialogState({ open: false });
          },
        }}
        title="Are you sure?"
        onClose={() => setConfirmationDialogState({ open: false })}
        styling={{ maxWidth: "32rem" }}
      >
        <Dialog.Content>
          <p className="text-sm text-zinc-600">
            {confirmationDialogState.open && confirmationDialogState.message}
          </p>
          <Dialog.Footer>
            <Button
              variant="secondary"
              onClick={() =>
                confirmationDialogState.open &&
                confirmationDialogState.onReject()
              }
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() =>
                confirmationDialogState.open &&
                confirmationDialogState.onConfirm()
              }
            >
              Continue
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog>
    </div>
  );
}

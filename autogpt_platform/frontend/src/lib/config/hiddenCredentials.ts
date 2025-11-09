/**
 * Hidden system credentials configuration
 * 
 * These are built-in "Use Credits for X" credentials that should be hidden from the UI.
 * Configured via environment variables to avoid hardcoding IDs in source code.
 * 
 * Usage:
 * ```typescript
 * import { HIDDEN_CREDENTIAL_IDS } from '@/lib/config/hiddenCredentials';
 * 
 * const isHidden = HIDDEN_CREDENTIAL_IDS.includes(credentialId);
 * ```
 */

/**
 * Array of credential IDs that should be hidden from the integrations page.
 * These represent system-level credentials that users shouldn't manage directly.
 */
export const HIDDEN_CREDENTIAL_IDS: string[] = [
  // AI/ML Providers
  process.env.NEXT_PUBLIC_HIDDEN_CRED_OLLAMA,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_OPENAI,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_ANTHROPIC,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_GROQ,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_REPLICATE,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_AIML,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_OPEN_ROUTER,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_NVIDIA,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_LLAMA_API,

  // Media/Content Generation
  process.env.NEXT_PUBLIC_HIDDEN_CRED_REVID,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_IDEOGRAM,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_DID,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_UNREAL_SPEECH,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_FAL,

  // Data/Search/Tools
  process.env.NEXT_PUBLIC_HIDDEN_CRED_JINA,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_EXA,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_E2B,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_MEM0,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_APOLLO,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_GOOGLE_MAPS,

  // Marketing/Communication
  process.env.NEXT_PUBLIC_HIDDEN_CRED_SMARTLEAD,
  process.env.NEXT_PUBLIC_HIDDEN_CRED_ZEROBOUNCE,
].filter((id): id is string => id !== undefined && id !== "");

/**
 * Fallback credential IDs if environment variables are not configured.
 * These are the original hardcoded values for backward compatibility.
 * 
 * @deprecated Use environment variables instead (see .env.example)
 */
export const FALLBACK_HIDDEN_CREDENTIAL_IDS: string[] = [
  "744fdc56-071a-4761-b5a5-0af0ce10a2b5", // Ollama
  "fdb7f412-f519-48d1-9b5f-d2f73d0e01fe", // Revid
  "760f84fc-b270-42de-91f6-08efe1b512d0", // Ideogram
  "6b9fc200-4726-4973-86c9-cd526f5ce5db", // Replicate
  "53c25cb8-e3ee-465c-a4d1-e75a4c899c2a", // OpenAI
  "24e5d942-d9e3-4798-8151-90143ee55629", // Anthropic
  "aad82a89-9794-4ebb-977f-d736aa5260a3", // AI/ML
  "4ec22295-8f97-4dd1-b42b-2c6957a02545", // Groq
  "7f7b0654-c36b-4565-8fa7-9a52575dfae2", // D-ID
  "7f26de70-ba0d-494e-ba76-238e65e7b45f", // Jina
  "66f20754-1b81-48e4-91d0-f4f0dd82145f", // Unreal Speech
  "b5a0e27d-0c98-4df3-a4b9-10193e1f3c40", // Open Router
  "6c0f5bd0-9008-4638-9d79-4b40b631803e", // FAL
  "96153e04-9c6c-4486-895f-5bb683b1ecec", // Exa
  "78d19fd7-4d59-4a16-8277-3ce310acf2b7", // E2B
  "96b83908-2789-4dec-9968-18f0ece4ceb3", // Nvidia
  "ed55ac19-356e-4243-a6cb-bc599e9b716f", // Mem0
  "544c62b5-1d0f-4156-8fb4-9525f11656eb", // Apollo
  "3bcdbda3-84a3-46af-8fdb-bfd2472298b8", // SmartLead
  "63a6e279-2dc2-448e-bf57-85776f7176dc", // ZeroBounce
  "9aa1bde0-4947-4a70-a20c-84daa3850d52", // Google Maps
  "d44045af-1c33-4833-9e19-752313214de2", // Llama API
];

/**
 * Get the list of hidden credential IDs, using env variables with fallback.
 * 
 * @returns Array of credential IDs to hide
 */
export function getHiddenCredentialIds(): string[] {
  return HIDDEN_CREDENTIAL_IDS.length > 0
    ? HIDDEN_CREDENTIAL_IDS
    : FALLBACK_HIDDEN_CREDENTIAL_IDS;
}

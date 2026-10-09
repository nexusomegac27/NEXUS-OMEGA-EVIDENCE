import { createFileRoute } from "@tanstack/react-router";
import { RelayConsole } from "@/components/relay-console";
import { readDocumentaryCycle } from "@/lib/relay/cycle";

export const Route = createFileRoute("/")({
  // Documentary only — no auto NOAA GET on page load / refresh.
  // Live SMOKE_ONLY fetch requires explicit click → readOfficialCycle.
  loader: () => readDocumentaryCycle(),
  component: Home,
});

function Home() {
  const initial = Route.useLoaderData();
  return <RelayConsole initial={initial} />;
}

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="mx-auto flex max-w-md flex-col items-center gap-4 text-center">
        <span className="font-display text-6xl font-extrabold text-primary/20">
          404
        </span>
        <h1 className="font-display text-2xl font-bold text-foreground">
          Pagina nu a fost găsită
        </h1>
        <p className="text-sm text-muted-foreground">
          Pagina pe care o cauți nu există sau a fost mutată.
        </p>
        <Button asChild variant="outline">
          <Link href="/marketing-pentru-turism">
            <ArrowLeft className="size-4" />
            Înapoi la pagina principală
          </Link>
        </Button>
      </div>
    </div>
  );
}

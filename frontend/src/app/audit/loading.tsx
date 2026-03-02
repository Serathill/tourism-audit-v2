import { Skeleton } from "@/components/ui/skeleton";

export default function AuditLoading() {
  return (
    <div className="bg-gradient-hero">
      <div className="mx-auto max-w-xl px-4 py-12 sm:px-6 md:py-16">
        <div className="mb-8 flex flex-col items-center gap-3">
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-5 w-2/3" />
        </div>
        <Skeleton className="h-[450px] rounded-2xl" />
      </div>
    </div>
  );
}

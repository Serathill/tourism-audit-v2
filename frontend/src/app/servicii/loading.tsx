import { Skeleton } from "@/components/ui/skeleton";

export default function ServiciiLoading() {
  return (
    <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16">
      <div className="mb-10 text-center">
        <Skeleton className="mx-auto h-9 w-56" />
        <Skeleton className="mx-auto mt-3 h-5 w-80" />
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-xl border border-border p-6">
            <Skeleton className="mb-4 h-6 w-24" />
            <Skeleton className="mb-2 h-8 w-32" />
            <Skeleton className="mb-4 h-4 w-full" />
            <div className="flex flex-col gap-2">
              {[1, 2, 3, 4].map((j) => (
                <Skeleton key={j} className="h-4 w-full" />
              ))}
            </div>
            <Skeleton className="mt-6 h-10 w-full rounded-lg" />
          </div>
        ))}
      </div>
    </div>
  );
}

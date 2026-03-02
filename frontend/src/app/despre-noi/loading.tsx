import { Skeleton } from "@/components/ui/skeleton";

export default function DespreNoiLoading() {
  return (
    <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16">
      <div className="mb-10 text-center">
        <Skeleton className="mx-auto h-9 w-48" />
        <Skeleton className="mx-auto mt-3 h-5 w-72" />
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="rounded-xl border border-border p-6">
            <div className="flex flex-col items-center gap-3">
              <Skeleton className="size-24 rounded-full" />
              <Skeleton className="h-5 w-36" />
              <Skeleton className="h-4 w-24" />
              <Skeleton className="mt-2 h-16 w-full" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

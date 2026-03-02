import { Skeleton } from "@/components/ui/skeleton";

export default function MarketingLoading() {
  return (
    <div className="flex flex-col">
      {/* Hero skeleton */}
      <div className="bg-gradient-hero">
        <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6 md:py-16 lg:py-20">
          <div className="grid gap-10 lg:grid-cols-[1.2fr_1fr] lg:gap-16">
            <div className="flex flex-col gap-6">
              <Skeleton className="h-10 w-3/4" />
              <Skeleton className="h-6 w-full" />
              <Skeleton className="h-6 w-2/3" />
              <div className="flex items-center gap-3">
                <div className="flex -space-x-2">
                  <Skeleton className="size-10 rounded-full" />
                  <Skeleton className="size-10 rounded-full" />
                  <Skeleton className="size-10 rounded-full" />
                </div>
                <Skeleton className="h-4 w-40" />
              </div>
            </div>
            <Skeleton className="h-[400px] rounded-2xl" />
          </div>
        </div>
      </div>

      {/* Sections skeleton */}
      {[1, 2, 3].map((i) => (
        <div key={i} className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6">
          <Skeleton className="mx-auto mb-10 h-8 w-2/3" />
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <Skeleton className="h-48 rounded-xl" />
            <Skeleton className="h-48 rounded-xl" />
            <Skeleton className="h-48 rounded-xl" />
          </div>
        </div>
      ))}
    </div>
  );
}

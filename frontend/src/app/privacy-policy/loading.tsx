import { Skeleton } from "@/components/ui/skeleton";

export default function PrivacyPolicyLoading() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
      <Skeleton className="mb-8 h-9 w-64" />
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="mb-6">
          <Skeleton className="mb-3 h-6 w-48" />
          <Skeleton className="mb-2 h-4 w-full" />
          <Skeleton className="mb-2 h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
        </div>
      ))}
    </div>
  );
}

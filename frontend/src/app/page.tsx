import { redirect } from "next/navigation";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Audit Digital Gratuit pentru Turism | DeviDevs Agency",
  alternates: { canonical: "/" },
};

export default function HomePage() {
  redirect("/marketing-pentru-turism");
}

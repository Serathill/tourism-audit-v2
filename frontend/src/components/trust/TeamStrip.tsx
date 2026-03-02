import Image from "next/image";
import { TEAM_MEMBERS } from "@/lib/constants";

export function TeamStrip() {
  return (
    <div className="flex items-center gap-3">
      {/* Overlapping team photos */}
      <div className="flex -space-x-2">
        {TEAM_MEMBERS.map((member) => (
          <div
            key={member.name}
            className="relative size-10 overflow-hidden rounded-full border-2 border-primary ring-2 ring-white"
          >
            <Image
              src={member.image}
              alt={member.name}
              fill
              sizes="40px"
              className="object-cover"
            />
          </div>
        ))}
      </div>
      {/* Label */}
      <p className="text-sm text-muted-foreground">
        <span className="font-medium text-foreground">Alexandru, Petru &amp; Nicu</span>
        {" "}— echipa DeviDevs
      </p>
    </div>
  );
}

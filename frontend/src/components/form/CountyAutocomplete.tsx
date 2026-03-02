"use client";

import { useState, useRef, useEffect } from "react";
import { Check, ChevronDown, Search } from "lucide-react";
import { REGIONS } from "@/lib/constants";
import { cn } from "@/lib/utils";

type CountyAutocompleteProps = {
  value: string;
  onChange: (value: string) => void;
  error?: string;
};

export function CountyAutocomplete({
  value,
  onChange,
  error,
}: CountyAutocompleteProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    if (open) {
      document.addEventListener("mousedown", handleClick);
      return () => document.removeEventListener("mousedown", handleClick);
    }
  }, [open]);

  // Focus search when opening
  useEffect(() => {
    if (open) {
      // Small delay to let the dropdown render
      requestAnimationFrame(() => searchRef.current?.focus());
    } else {
      setSearch("");
    }
  }, [open]);

  const filteredRegions = REGIONS.map((region) => ({
    ...region,
    counties: region.counties.filter((county) =>
      county.toLowerCase().includes(search.toLowerCase())
    ),
  })).filter((region) => region.counties.length > 0);

  return (
    <div ref={containerRef} className="relative">
      {/* Trigger button */}
      <button
        type="button"
        role="combobox"
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-invalid={!!error}
        onClick={() => setOpen(!open)}
        className={cn(
          "flex h-11 w-full items-center justify-between rounded-[var(--radius-md)] border bg-transparent px-3 py-2 text-base shadow-xs transition-[color,box-shadow] outline-none md:text-sm",
          "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
          error
            ? "border-destructive ring-destructive/20"
            : "border-input",
          value ? "text-foreground" : "text-muted-foreground"
        )}
      >
        {value || "Selectează județul"}
        <ChevronDown className={cn("size-4 shrink-0 text-muted-foreground transition-transform", open && "rotate-180")} />
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute z-50 mt-1 w-full rounded-lg border border-border bg-white shadow-lg">
          {/* Search input */}
          <div className="flex items-center gap-2 border-b border-border px-3 py-2">
            <Search className="size-4 text-muted-foreground" />
            <input
              ref={searchRef}
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Caută..."
              className="h-8 w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground"
            />
          </div>

          {/* Options list */}
          <div role="listbox" className="max-h-60 overflow-y-auto p-1">
            {filteredRegions.length === 0 ? (
              <p className="px-3 py-4 text-center text-sm text-muted-foreground">
                Niciun județ găsit
              </p>
            ) : (
              filteredRegions.map((region) => (
                <div key={region.name}>
                  <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
                    {region.name}
                  </div>
                  {region.counties.map((county) => (
                    <button
                      key={county}
                      type="button"
                      role="option"
                      aria-selected={value === county}
                      onClick={() => {
                        onChange(county);
                        setOpen(false);
                      }}
                      className={cn(
                        "flex w-full items-center justify-between rounded-md px-2 py-2 text-sm transition-colors",
                        value === county
                          ? "bg-primary/10 text-primary font-medium"
                          : "text-foreground hover:bg-muted"
                      )}
                    >
                      {county}
                      {value === county && (
                        <Check className="size-4 text-primary" />
                      )}
                    </button>
                  ))}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

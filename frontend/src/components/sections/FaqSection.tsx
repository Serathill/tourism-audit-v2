"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

const FAQS = [
  {
    question: "De ce este auditul gratuit? Care e 'șmecheria'?",
    answer:
      "Nu există nicio 'șmecherie'. Auditul gratuit este modul nostru de a demonstra ce putem face. Vrem să vezi concret valoarea analizei noastre înainte de orice discuție despre colaborare. Nu ai nicio obligație după audit.",
  },
  {
    question: "Ce se întâmplă, concret, după ce solicit auditul?",
    answer:
      "Completezi formularul (durează ~2 minute), iar noi analizăm prezența ta online folosind doar informații publice. În 30-90 de minute primești pe email un raport detaliat cu recomandări personalizate. După aceea, dacă dorești, programăm o discuție gratuită de follow-up.",
  },
  {
    question: "Sunt obligat(ă) să cumpăr ceva după audit?",
    answer:
      "Nu. Auditul și discuția de follow-up sunt 100% gratuite, fără nicio obligație. Dacă îți plac recomandările noastre și vrei să mergem mai departe, discutăm opțiunile. Dacă nu, păstrezi raportul și îl folosești cum dorești.",
  },
  {
    question: "Acest serviciu este pentru mine dacă nu am o echipă de marketing?",
    answer:
      "Da, exact pentru tine este. Majoritatea proprietarilor de pensiuni și case de vacanță nu au o echipă dedicată de marketing. Auditul îți arată clar ce poți îmbunătăți, iar dacă decizi să colaborăm, noi preluăm totul.",
  },
  {
    question: "Aveți nevoie de acces la conturile mele?",
    answer:
      "Nu. Nu cerem parole, acces la conturi sau date financiare. Tot procesul de audit se bazează pe informații publice disponibile online. Este complet sigur și transparent.",
  },
  {
    question: "În cât timp pot vedea rezultate?",
    answer:
      "Raportul de audit ajunge pe email în 30-90 de minute. Dacă decizi să implementezi recomandările (singur sau cu noi), primele îmbunătățiri ale vizibilității online se văd de obicei în 4-8 săptămâni.",
  },
  {
    question: "Ce tipuri de proprietăți ați analizat până acum?",
    answer:
      "Am lucrat cu pensiuni boutique, tiny houses, A-frames, glampinguri, hoteluri de 3-4 stele și case de vacanță din toată România. Auditul nostru se adaptează la orice tip de unitate de cazare, de la o cabană în pădure la un hotel de oraș.",
  },
] as const;

export function FaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section aria-labelledby="faq-heading" className="bg-white">
      <div className="mx-auto max-w-[1200px] px-4 py-16 sm:px-6 md:py-20">
        <h2
          id="faq-heading"
          className="mb-10 text-center font-display text-[clamp(1.5rem,3vw,2rem)] font-bold tracking-tight text-foreground"
        >
          Întrebări frecvente
        </h2>

        <div className="mx-auto max-w-2xl divide-y divide-border">
          {FAQS.map((faq, index) => {
            const isOpen = openIndex === index;
            return (
              <div key={index} className="py-4">
                <button
                  type="button"
                  id={`faq-question-${index}`}
                  className="flex w-full items-center justify-between gap-4 text-left"
                  onClick={() => setOpenIndex(isOpen ? null : index)}
                  aria-expanded={isOpen}
                  aria-controls={`faq-answer-${index}`}
                >
                  <span className="font-medium text-foreground">
                    {faq.question}
                  </span>
                  <ChevronDown
                    className={`size-5 shrink-0 text-muted-foreground transition-transform duration-200 ${
                      isOpen ? "rotate-180" : ""
                    }`}
                  />
                </button>
                <div
                  id={`faq-answer-${index}`}
                  role="region"
                  aria-labelledby={`faq-question-${index}`}
                  className={`overflow-hidden transition-all duration-200 ${
                    isOpen ? "mt-3 max-h-96" : "max-h-0"
                  }`}
                >
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {faq.answer}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

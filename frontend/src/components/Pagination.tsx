import React from "react";
export default function Pagination({ page, pages, onPrev, onNext }:{ page:number; pages:number; onPrev:()=>void; onNext:()=>void }){
  return (
    <div className="flex items-center gap-2">
      <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" onClick={onPrev} disabled={page<=1}>Prev</button>
      <span>Page {page} / {pages}</span>
      <button className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50" onClick={onNext} disabled={page>=pages}>Next</button>
    </div>
  );
}

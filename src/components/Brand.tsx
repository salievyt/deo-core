export function Mark({ className = "" }: { className?: string }) {
  return (
    <svg
      className={className}
      width="30"
      height="30"
      viewBox="0 0 30 30"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M12 0h6v9l6.36-6.36 4.24 4.24L22.24 13H30v6h-9l6.36 6.36-4.24 4.24L17 23.24V30h-6v-9l-6.36 6.36L.4 23.12 6.76 17H0v-6h9L2.64 4.64 6.88.4 13 6.76V0Z"
        fill="currentColor"
      />
    </svg>
  );
}
export function Brand() {
  return (
    <span className="brand">
      <Mark />
      <span>
        DEO CORE<span className="brand-dot">®</span>
      </span>
    </span>
  );
}

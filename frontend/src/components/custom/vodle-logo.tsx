interface VodleLogoProps {
  size?: 'small' | 'medium' | 'large';
}

export function VodleLogo({ size = 'medium' }: VodleLogoProps) {
  const fontSize = {
    small: '1.5rem',
    medium: '2rem',
    large: '3.5rem',
  };

  const fontWeight = {
    small: '600',
    medium: '600',
    large: '700',
  };

  return (
    <h1
      style={{
        fontSize: fontSize[size],
        fontWeight: fontWeight[size],
        letterSpacing: '-0.02em',
      }}
    >
      Vodle
    </h1>
  );
}




// interface VodleLogoProps {
//   size?: 'small' | 'medium' | 'large';
//   variant?: 'default' | 'compact';
// }

// export function VodleLogo({ size = 'medium', variant = 'default' }: VodleLogoProps) {
//   const dimensions = {
//     small: { icon: 32, text: '1.25rem' },
//     medium: { icon: 48, text: '2rem' },
//     large: { icon: 64, text: '3.5rem' },
//   };

//   const iconSize = dimensions[size].icon;
//   const textSize = dimensions[size].text;

//   if (variant === 'compact') {
//     return (
//       <div className="flex items-center gap-3">
//         {/* Globe Vote Icon */}
//         <svg
//           width={iconSize}
//           height={iconSize}
//           viewBox="0 0 48 48"
//           fill="none"
//           xmlns="http://www.w3.org/2000/svg"
//         >
//           {/* Outer circle - globe */}
//           <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="1.5" fill="none" />

//           {/* Latitude lines */}
//           <ellipse cx="24" cy="24" rx="20" ry="8" stroke="currentColor" strokeWidth="0.8" opacity="0.4" fill="none" />
//           <ellipse cx="24" cy="24" rx="20" ry="14" stroke="currentColor" strokeWidth="0.8" opacity="0.3" fill="none" />

//           {/* Longitude line */}
//           <ellipse cx="24" cy="24" rx="8" ry="20" stroke="currentColor" strokeWidth="0.8" opacity="0.4" fill="none" />

//           {/* Central V checkmark */}
//           <path
//             d="M18 22 L22 28 L30 18"
//             stroke="currentColor"
//             strokeWidth="2.5"
//             strokeLinecap="round"
//             strokeLinejoin="round"
//           />
//         </svg>

//         <span
//           className="tracking-tight"
//           style={{
//             fontSize: textSize,
//             fontWeight: '600',
//             letterSpacing: '-0.02em',
//           }}
//         >
//           Vodle
//         </span>
//       </div>
//     );
//   }

//   return (
//     <div className="flex flex-col items-center gap-6">
//       {/* Main Icon */}
//       <svg
//         width={iconSize * 1.5}
//         height={iconSize * 1.5}
//         viewBox="0 0 72 72"
//         fill="none"
//         xmlns="http://www.w3.org/2000/svg"
//       >
//         {/* Background gradient circle */}
//         <defs>
//           <linearGradient id="vodle-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
//             <stop offset="0%" stopColor="currentColor" stopOpacity="0.1" />
//             <stop offset="100%" stopColor="currentColor" stopOpacity="0.05" />
//           </linearGradient>
//         </defs>

//         <circle cx="36" cy="36" r="32" fill="url(#vodle-gradient)" />

//         {/* Globe structure */}
//         <circle cx="36" cy="36" r="28" stroke="currentColor" strokeWidth="2" fill="none" />

//         {/* Latitude lines */}
//         <ellipse cx="36" cy="36" rx="28" ry="12" stroke="currentColor" strokeWidth="1.2" opacity="0.5" fill="none" />
//         <ellipse cx="36" cy="36" rx="28" ry="20" stroke="currentColor" strokeWidth="1.2" opacity="0.3" fill="none" />

//         {/* Longitude lines */}
//         <ellipse cx="36" cy="36" rx="12" ry="28" stroke="currentColor" strokeWidth="1.2" opacity="0.5" fill="none" />
//         <ellipse cx="36" cy="36" rx="20" ry="28" stroke="currentColor" strokeWidth="1.2" opacity="0.3" fill="none" />

//         {/* Central V/Check symbol */}
//         <path
//           d="M26 33 L32 42 L46 24"
//           stroke="currentColor"
//           strokeWidth="3.5"
//           strokeLinecap="round"
//           strokeLinejoin="round"
//         />

//         {/* Accent dots around the globe */}
//         <circle cx="36" cy="8" r="2" fill="currentColor" opacity="0.6" />
//         <circle cx="64" cy="36" r="2" fill="currentColor" opacity="0.6" />
//         <circle cx="36" cy="64" r="2" fill="currentColor" opacity="0.6" />
//         <circle cx="8" cy="36" r="2" fill="currentColor" opacity="0.6" />
//       </svg>

//       {/* Wordmark */}
//       <h1
//         className="tracking-tight"
//         style={{
//           fontSize: textSize,
//           fontWeight: '600',
//           letterSpacing: '-0.02em',
//         }}
//       >
//         Vodle
//       </h1>

//       {/* Tagline */}
//       <p className="text-xs text-muted-foreground uppercase tracking-widest" style={{ letterSpacing: '0.2em' }}>
//         Voice Your Opinion
//       </p>
//     </div>
//   );
// }

// // interface VodleLogoProps {
// //   size?: "small" | "medium" | "large";
// //   variant?: "default" | "compact";
// // }

// // export function VodleLogo({
// //   size = "medium",
// //   variant = "default",
// // }: VodleLogoProps) {
// //   const sizeClasses = {
// //     small: "text-xl",
// //     medium: "text-[2rem]",
// //     large: "text-[3.5rem]",
// //   };

// //   const sharedTextStyle = {
// //     fontWeight: "300",
// //     letterSpacing: "0.15em",
// //     fontFamily: "'Playfair Display', serif",
// //   } as const;

// //   const iconSize =
// //     size === "small" ? "24" : size === "medium" ? "32" : "48";

// //   if (variant === "compact") {
// //     return (
// //       <div className="flex items-center gap-2 transition-transform hover:scale-105">
// //         <div className="relative">
// //           <svg
// //             width={iconSize}
// //             height={iconSize}
// //             viewBox="0 0 40 40"
// //             fill="none"
// //             xmlns="http://www.w3.org/2000/svg"
// //           >
// //             <rect
// //               x="2"
// //               y="2"
// //               width="36"
// //               height="36"
// //               stroke="currentColor"
// //               strokeWidth="0.5"
// //               fill="none"
// //             />

// //             <path
// //               d="M12 10 L20 26 L28 10"
// //               stroke="currentColor"
// //               strokeWidth="1.5"
// //               strokeLinecap="round"
// //               strokeLinejoin="round"
// //               fill="none"
// //             />

// //             <circle cx="10" cy="30" r="0.75" fill="currentColor" />
// //             <circle cx="30" cy="30" r="0.75" fill="currentColor" />
// //           </svg>
// //         </div>

// //         <span className={`tracking-widest ${sizeClasses[size]}`} style={sharedTextStyle}>
// //           VODLE
// //         </span>
// //       </div>
// //     );
// //   }

// //   return (
// //     <div className="flex flex-col items-center gap-3">
// //       <div className="relative">
// //         <h1 className={`tracking-widest ${sizeClasses[size]}`} style={sharedTextStyle}>
// //           VODLE
// //         </h1>

// //         <div className="absolute -bottom-2 left-1/2 flex -translate-x-1/2 transform items-center gap-1">
// //           <div className="h-px w-8 bg-current opacity-40" />
// //           <div className="h-1 w-1 rounded-full bg-current opacity-60" />
// //           <div className="h-px w-8 bg-current opacity-40" />
// //         </div>
// //       </div>
// //     </div>
// //   );
// // }

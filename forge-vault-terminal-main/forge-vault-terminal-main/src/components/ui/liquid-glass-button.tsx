"use client";

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const liquidbuttonVariants = cva(
  "inline-flex items-center justify-center cursor-pointer gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-[color,box-shadow] disabled:pointer-events-none disabled:opacity-50 outline-none",
  {
    variants: {
      variant: {
        default: "bg-transparent hover:scale-105 duration-300 transition text-primary",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 text-xs gap-1.5 px-4",
        lg: "h-10 rounded-md px-6",
        xl: "h-12 rounded-md px-8",
        xxl: "h-14 rounded-md px-10",
        icon: "size-9",
      },
    },
    defaultVariants: { variant: "default", size: "xxl" },
  }
);

function GlassFilter() {
  return (
    <svg className="hidden">
      <defs>
        <filter id="liquid-lens" x="-50%" y="-50%" width="200%" height="200%" colorInterpolationFilters="sRGB">
          <feTurbulence type="fractalNoise" baseFrequency="0.05 0.05" numOctaves="1" seed="5" result="turb" />
          <feGaussianBlur in="turb" stdDeviation="2" result="blurred" />
          <feDisplacementMap in="SourceGraphic" in2="blurred" scale="70" xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </defs>
    </svg>
  );
}

export function LiquidButton({
  className,
  variant,
  size,
  asChild = false,
  children,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof liquidbuttonVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "button";
  return (
    <>
      <Comp className={cn(liquidbuttonVariants({ variant, size, className }), "relative overflow-hidden")} {...props}>
        <span className="relative z-10">{children}</span>
      </Comp>
      <GlassFilter />
    </>
  );
}

type ColorVariant = "default" | "primary" | "success" | "error" | "gold" | "bronze";

interface MetalButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ColorVariant;
}

const colorVariants: Record<
  ColorVariant,
  { outer: string; inner: string; button: string; textColor: string; textShadow: string }
> = {
  default: {
    outer: "bg-gradient-to-b from-[#000] to-[#A0A0A0]",
    inner: "bg-gradient-to-b from-[#FAFAFA] via-[#3E3E3E] to-[#E5E5E5]",
    button: "bg-gradient-to-b from-[#B9B9B9] to-[#969696]",
    textColor: "text-white",
    textShadow: "[text-shadow:_0_-1px_0_rgb(80_80_80_/_100%)]",
  },
  primary: {
    outer: "bg-gradient-to-b from-[#000] to-[#A0A0A0]",
    inner: "bg-gradient-to-b from-primary via-secondary to-muted",
    button: "bg-gradient-to-b from-primary to-primary/40",
    textColor: "text-white",
    textShadow: "[text-shadow:_0_-1px_0_rgb(30_58_138_/_100%)]",
  },
  success: {
    outer: "bg-gradient-to-b from-[#005A43] to-[#7CCB9B]",
    inner: "bg-gradient-to-b from-[#E5F8F0] via-[#00352F] to-[#D1F0E6]",
    button: "bg-gradient-to-b from-[#9ADBC8] to-[#3E8F7C]",
    textColor: "text-[#FFF7F0]",
    textShadow: "[text-shadow:_0_-1px_0_rgb(6_78_59_/_100%)]",
  },
  error: {
    outer: "bg-gradient-to-b from-[#5A0000] to-[#FFAEB0]",
    inner: "bg-gradient-to-b from-[#FFDEDE] via-[#680002] to-[#FFE9E9]",
    button: "bg-gradient-to-b from-[#F08D8F] to-[#A45253]",
    textColor: "text-[#FFF7F0]",
    textShadow: "[text-shadow:_0_-1px_0_rgb(146_64_14_/_100%)]",
  },
  gold: {
    outer: "bg-gradient-to-b from-[#917100] to-[#EAD98F]",
    inner: "bg-gradient-to-b from-[#FFFDDD] via-[#856807] to-[#FFF1B3]",
    button: "bg-gradient-to-b from-[#FFEBA1] to-[#9B873F]",
    textColor: "text-[#FFFDE5]",
    textShadow: "[text-shadow:_0_-1px_0_rgb(178_140_2_/_100%)]",
  },
  bronze: {
    outer: "bg-gradient-to-b from-[#864813] to-[#E9B486]",
    inner: "bg-gradient-to-b from-[#EDC5A1] via-[#5F2D01] to-[#FFDEC1]",
    button: "bg-gradient-to-b from-[#FFE3C9] to-[#A36F3D]",
    textColor: "text-[#FFF7F0]",
    textShadow: "[text-shadow:_0_-1px_0_rgb(124_45_18_/_100%)]",
  },
};

export const MetalButton = React.forwardRef<HTMLButtonElement, MetalButtonProps>(
  ({ children, className, variant = "default", disabled, ...props }, ref) => {
    const [isPressed, setIsPressed] = React.useState(false);
    const [isHovered, setIsHovered] = React.useState(false);
    const [isTouchDevice, setIsTouchDevice] = React.useState(false);

    React.useEffect(() => {
      setIsTouchDevice("ontouchstart" in window || navigator.maxTouchPoints > 0);
    }, []);

    const colors = colorVariants[variant];
    const transitionStyle = "all 250ms cubic-bezier(0.1, 0.4, 0.2, 1)";

    const wrapperStyle: React.CSSProperties = {
      transform: isPressed ? "translateY(2.5px) scale(0.99)" : "translateY(0) scale(1)",
      boxShadow: isPressed
        ? "0 1px 2px rgba(0,0,0,0.15)"
        : isHovered && !isTouchDevice
        ? "0 4px 12px rgba(0,0,0,0.12)"
        : "0 3px 8px rgba(0,0,0,0.08)",
      transition: transitionStyle,
      opacity: disabled ? 0.5 : 1,
    };
    const innerStyle: React.CSSProperties = {
      transition: transitionStyle,
      filter: isHovered && !isPressed && !isTouchDevice ? "brightness(1.05)" : "none",
    };
    const buttonStyle: React.CSSProperties = {
      transform: isPressed ? "scale(0.97)" : "scale(1)",
      transition: transitionStyle,
      filter: isHovered && !isPressed && !isTouchDevice ? "brightness(1.02)" : "none",
    };

    return (
      <div
        className={cn("relative inline-flex transform-gpu rounded-md p-[1.25px]", colors.outer, disabled && "pointer-events-none")}
        style={wrapperStyle}
        onMouseEnter={() => !isTouchDevice && setIsHovered(true)}
        onMouseLeave={() => {
          setIsHovered(false);
          setIsPressed(false);
        }}
        onMouseDown={() => setIsPressed(true)}
        onMouseUp={() => setIsPressed(false)}
        onTouchStart={() => setIsPressed(true)}
        onTouchEnd={() => setIsPressed(false)}
        onTouchCancel={() => setIsPressed(false)}
      >
        <div className={cn("absolute inset-[1px] rounded-md", colors.inner)} style={innerStyle} />
        <button
          ref={ref}
          disabled={disabled}
          className={cn(
            "relative z-10 m-[1px] inline-flex h-11 cursor-pointer items-center justify-center overflow-hidden rounded-md px-6 py-2 text-sm font-semibold outline-none disabled:cursor-not-allowed",
            colors.button,
            colors.textColor,
            colors.textShadow,
            className
          )}
          style={buttonStyle}
          {...props}
        >
          {children}
        </button>
      </div>
    );
  }
);
MetalButton.displayName = "MetalButton";

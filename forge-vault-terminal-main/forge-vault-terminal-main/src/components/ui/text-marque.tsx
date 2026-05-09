"use client";
import { useRef, useEffect, forwardRef } from "react";
import {
  motion,
  useScroll,
  useSpring,
  useTransform,
  useVelocity,
  useAnimationFrame,
  useMotionValue,
} from "motion/react";
import { wrap } from "@motionone/utils";
import { cn } from "@/lib/utils";

interface MarqueeProps {
  children: string;
  baseVelocity?: number;
  className?: string;
  scrollDependent?: boolean;
  delay?: number;
}

const TextMarquee = forwardRef<HTMLDivElement, MarqueeProps>(
  ({ children, baseVelocity = -5, className, scrollDependent = false, delay = 0 }, ref) => {
    const baseX = useMotionValue(0);
    const { scrollY } = useScroll();
    const scrollVelocity = useVelocity(scrollY);
    const smoothVelocity = useSpring(scrollVelocity, { damping: 50, stiffness: 400 });
    const velocityFactor = useTransform(smoothVelocity, [0, 1000], [0, 2], { clamp: false });
    const x = useTransform(baseX, (v) => `${wrap(-20, -45, v)}%`);
    const directionFactor = useRef(1);
    const hasStarted = useRef(false);

    useEffect(() => {
      const t = setTimeout(() => { hasStarted.current = true; }, delay);
      return () => clearTimeout(t);
    }, [delay]);

    useAnimationFrame((_t, delta) => {
      if (!hasStarted.current) return;
      let moveBy = directionFactor.current * baseVelocity * (delta / 1000);
      if (scrollDependent) {
        if (velocityFactor.get() < 0) directionFactor.current = -1;
        else if (velocityFactor.get() > 0) directionFactor.current = 1;
      }
      moveBy += directionFactor.current * moveBy * velocityFactor.get();
      baseX.set(baseX.get() + moveBy);
    });

    return (
      <div ref={ref} className="overflow-hidden whitespace-nowrap">
        <motion.div className={cn("flex whitespace-nowrap", className)} style={{ x }}>
          <span className="block pr-12">{children}</span>
          <span className="block pr-12">{children}</span>
          <span className="block pr-12">{children}</span>
          <span className="block pr-12">{children}</span>
        </motion.div>
      </div>
    );
  }
);
TextMarquee.displayName = "TextMarquee";

export default TextMarquee;
export { TextMarquee };

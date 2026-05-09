"use client";

import { Check, ChevronDown } from "lucide-react";
import {
  Button as AriaButton,
  ButtonProps as AriaButtonProps,
  ListBox as AriaListBox,
  ListBoxItem as AriaListBoxItem,
  ListBoxItemProps as AriaListBoxItemProps,
  ListBoxProps as AriaListBoxProps,
  Popover as AriaPopover,
  PopoverProps as AriaPopoverProps,
  Select as AriaSelect,
  SelectProps as AriaSelectProps,
  SelectValue as AriaSelectValue,
  SelectValueProps as AriaSelectValueProps,
  composeRenderProps,
} from "react-aria-components";
import { cn } from "@/lib/utils";

export const Select = AriaSelect;

export const SelectValue = <T extends object>({
  className,
  ...props
}: AriaSelectValueProps<T>) => (
  <AriaSelectValue
    className={composeRenderProps(className, (c) =>
      cn("line-clamp-1 data-[placeholder]:text-white/40", c),
    )}
    {...props}
  />
);

export const SelectTrigger = ({ className, children, ...props }: AriaButtonProps) => (
  <AriaButton
    className={composeRenderProps(className, (c) =>
      cn(
        "flex h-11 w-full items-center justify-between rounded-md border border-white/10 bg-white/[0.03] px-4 py-2 text-sm text-white outline-none transition",
        "data-[hovered]:border-white/30 data-[hovered]:bg-white/[0.06]",
        "data-[focus-visible]:border-white/40 data-[focus-visible]:ring-2 data-[focus-visible]:ring-white/20",
        "data-[open]:border-white/40 data-[open]:bg-white/[0.06]",
        "data-[disabled]:cursor-not-allowed data-[disabled]:opacity-50",
        c,
      ),
    )}
    {...props}
  >
    {composeRenderProps(children, (ch) => (
      <>
        {ch}
        <ChevronDown aria-hidden="true" className="size-4 opacity-60" />
      </>
    ))}
  </AriaButton>
);

export const SelectPopover = ({ className, ...props }: AriaPopoverProps) => (
  <AriaPopover
    className={composeRenderProps(className, (c) =>
      cn(
        "w-[--trigger-width] rounded-md border border-white/10 bg-black/95 p-1 text-white shadow-[0_10px_40px_-10px_rgba(0,0,0,0.8)] backdrop-blur-xl outline-none",
        "data-[entering]:animate-in data-[entering]:fade-in-0 data-[entering]:zoom-in-95",
        "data-[exiting]:animate-out data-[exiting]:fade-out-0 data-[exiting]:zoom-out-95",
        c,
      ),
    )}
    {...props}
  />
);

export const SelectListBox = <T extends object>({
  className,
  ...props
}: AriaListBoxProps<T>) => (
  <AriaListBox
    className={composeRenderProps(className, (c) =>
      cn("max-h-[inherit] overflow-auto p-0 outline-none", c),
    )}
    {...props}
  />
);

export const SelectItem = ({ className, children, ...props }: AriaListBoxItemProps) => (
  <AriaListBoxItem
    className={composeRenderProps(className, (c) =>
      cn(
        "relative flex cursor-pointer select-none items-center gap-2 rounded px-3 py-2 text-sm text-white/80 outline-none transition",
        "data-[hovered]:bg-white/10 data-[hovered]:text-white",
        "data-[focused]:bg-white/10 data-[focused]:text-white",
        "data-[selected]:bg-white/15 data-[selected]:text-white",
        "data-[disabled]:cursor-not-allowed data-[disabled]:opacity-50",
        c,
      ),
    )}
    {...props}
  >
    {composeRenderProps(children, (ch, { isSelected }) => (
      <>
        <span className="flex-1">{ch}</span>
        {isSelected && <Check className="size-4 opacity-80" />}
      </>
    ))}
  </AriaListBoxItem>
);

interface JollySelectProps<T extends object>
  extends Omit<AriaSelectProps<T>, "children"> {
  items?: Iterable<T>;
  children: React.ReactNode | ((item: T) => React.ReactNode);
}

export function JollySelect<T extends object>({
  children,
  className,
  items,
  ...props
}: JollySelectProps<T>) {
  return (
    <Select
      className={composeRenderProps(className, (c) => cn("group flex w-full flex-col gap-2", c))}
      {...props}
    >
      <SelectTrigger>
        <SelectValue />
      </SelectTrigger>
      <SelectPopover>
        <SelectListBox items={items}>{children}</SelectListBox>
      </SelectPopover>
    </Select>
  );
}

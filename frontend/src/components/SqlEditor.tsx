import Editor from "@monaco-editor/react";
import { useAppStore } from "../store/useAppStore";

interface Props { value: string; onChange?: (v: string) => void; readOnly?: boolean; height?: string }

export default function SqlEditor({ value, onChange, readOnly, height = "200px" }: Props) {
  const dark = useAppStore((s) => s.dark);
  return (
    <Editor height={height} language="sql" theme={dark ? "vs-dark" : "light"} value={value}
      onChange={(v) => onChange?.(v ?? "")}
      options={{ readOnly, minimap: { enabled: false }, fontSize: 14, scrollBeyondLastLine: false }} />
  );
}

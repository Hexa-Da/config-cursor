/**
 * Plugin OpenCode — garde-fou sécurité (tool.execute.before).
 *
 * Délègue à garde-fou-opencode.py (même dossier ; classification partagée Cursor/jcode).
 * Chargé automatiquement depuis ~/.config/opencode/plugins/ après install-opencode.sh.
 */
import { spawnSync } from "node:child_process"
import { existsSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const WATCHED = new Set(["bash", "write", "edit", "multiedit", "apply_patch", "replace"])

function resolveScript() {
  return join(dirname(fileURLToPath(import.meta.url)), "garde-fou-opencode.py")
}

export const GardeFouPlugin = async ({ directory }) => {
  const script = resolveScript()

  return {
    "tool.execute.before": async (input, output) => {
      if (!WATCHED.has(input.tool)) return
      if (!existsSync(script)) {
        throw new Error(
          `Garde-fou : script introuvable (${script}). Relance install-opencode.sh.`,
        )
      }

      const payload = JSON.stringify({
        tool: input.tool,
        cwd: directory || "",
        args: output.args || {},
      })

      const result = spawnSync("python3", [script], {
        input: payload,
        encoding: "utf8",
        timeout: 15_000,
      })

      if (result.error) {
        throw new Error(`Garde-fou : échec python3 — ${result.error.message}`)
      }
      if (result.status === 0) return

      const message = (result.stderr || result.stdout || "Garde-fou DENY").trim()
      throw new Error(message || `Garde-fou DENY (exit ${result.status})`)
    },
  }
}

/**
 * Plugin OpenCode 2 — garde-fou sécurité (tool execute.before).
 *
 * Délègue à garde-fou-opencode.py (même dossier ; classification partagée avec Cursor).
 * Chargé automatiquement depuis ~/.config/opencode/plugins/ après install-opencode.sh.
 */
import { Plugin } from "@opencode/plugin"
import { spawnSync } from "node:child_process"
import { existsSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

/** Noms V2 + alias V1 encore possibles avant rewrite builtin. */
const WATCHED = new Set([
  "shell",
  "bash",
  "write",
  "edit",
  "multiedit",
  "patch",
  "apply_patch",
  "replace",
  "read",
])

function resolveScript() {
  return join(dirname(fileURLToPath(import.meta.url)), "garde-fou-opencode.py")
}

export default Plugin.define({
  id: "config-cursor.garde-fou",
  async setup(ctx) {
    const script = resolveScript()

    await ctx.tool.hook("execute.before", (event) => {
      if (!WATCHED.has(event.tool)) return
      if (!existsSync(script)) {
        throw new Error(
          `Garde-fou : script introuvable (${script}). Relance install-opencode.sh.`,
        )
      }

      const args =
        event.input && typeof event.input === "object" && !Array.isArray(event.input)
          ? event.input
          : {}

      const payload = JSON.stringify({
        tool: event.tool,
        cwd: ctx.location.directory || "",
        args,
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
    })
  },
})

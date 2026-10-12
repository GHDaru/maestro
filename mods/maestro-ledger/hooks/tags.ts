// The two tags the manager and the workers write. Each one ALONE on its own line:
//   [[TASK id=064-T03 kind=implement attempt=2 cycle=064 redoes=064-T03#1]]
//   [[DONE id=064-T03 outcome=delivered]]
//   [[DONE id=064-A01 outcome=delivered target=064-T03 verdict=rejected reason="no mutation evidence"]]
// A value with spaces goes in double quotes, and may contain `]`. Field names are lowercase.
//
// Why "alone on its line", and why first/last (independent review of cycle 065): a tag
// anywhere in the text meant that quoting the protocol's own example — in a pasted document,
// in an answer that explains it — clocked a fake task in, or closed the wrong one. The real
// [[TASK]] heads the assignment and the real [[DONE]] closes the delivery, so the FIRST
// own-line TASK and the LAST own-line DONE are the ones that count; the rest are quotations.

export type TagName = 'TASK' | 'DONE'
export type TagFields = Record<string, string>

// A quoted value may hold anything but a double quote, `]` included.
const PAIR = /([a-z_]+)=(?:"([^"]*)"|([^\s"\]]+))/g

function lineTag(line: string, name: TagName): TagFields | undefined {
  const match = new RegExp(`^\\s*\\[\\[${name}\\s+((?:[^\\]"]|"[^"]*")*)\\]\\]\\s*$`).exec(line)
  if (!match) return undefined
  const fields: TagFields = {}
  for (const pair of match[1].matchAll(PAIR)) fields[pair[1]] = pair[2] ?? pair[3]
  return fields.id ? fields : undefined
}

/** Every own-line `[[NAME ...]]` tag with an id, in the order they appear. */
export function parseTags(text: string, name: TagName): TagFields[] {
  const found: TagFields[] = []
  for (const line of text.split(/\r?\n/)) {
    const tag = lineTag(line, name)
    if (tag) found.push(tag)
  }
  return found
}

/** The tag that counts: the first own-line TASK, or the last own-line DONE. */
export function parseTag(text: string, name: TagName): TagFields | undefined {
  const tags = parseTags(text, name)
  return name === 'TASK' ? tags[0] : tags[tags.length - 1]
}

/** A positive integer, or undefined: `attempt=two` is not silently read as attempt 1. */
export function positiveInt(value: string | undefined): number | undefined {
  if (value === undefined || !/^[1-9][0-9]*$/.test(value)) return undefined
  return Number(value)
}

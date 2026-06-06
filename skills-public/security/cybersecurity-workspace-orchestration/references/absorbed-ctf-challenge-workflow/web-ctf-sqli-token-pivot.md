> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Web CTF SQL Injection Token-Pivot Pattern

## Session Context

In a Web CTF challenge, source review showed a vulnerable raw SQL insert similar to:

```js
await db.raw(
  `INSERT INTO secrets(owner_id, content) VALUES ('${userId}', '${content}')`
);
```

The user-controlled `content` field was interpolated directly into an `INSERT` statement. Because the stack allowed stacked queries, the exploit could terminate the string/value tuple and execute a second statement.

## Core Technique

A write-context SQL injection can be more valuable than a read-context SQL injection when auth/session state is stored in the same database.

Payload shape:

```sql
x'); UPDATE tokens
SET user_id = '<admin-user-id>'
WHERE id = '<attacker-auth-token>';--
```

After this, the attacker’s own token maps to the admin user. The next normal authenticated request reads admin-owned secrets/flag using the application’s legitimate session lookup.

## Why This Matters

- SQLi in `INSERT`/`UPDATE` paths is easy to overlook if you only test `SELECT` endpoints.
- Session/token tables are high-value targets; changing token ownership can be equivalent to account takeover.
- The exploit does not require knowing the admin password or stealing an admin cookie.
- A minimal CTF-safe exploit changes only the attacker’s own token row rather than dumping broad data.

## Review Checklist

When reviewing a Web CTF source bundle:

1. Search for raw SQL construction and template-string interpolation.
2. Determine whether stacked queries are supported by the DB/driver.
3. Identify seeded admin/test user IDs and token/session schema.
4. Check whether attacker-controlled input can execute an `UPDATE` against tokens/sessions/users/roles.
5. Prefer minimal proof: rebind own token/session, request the normal page, capture flag.

## Fix Pattern

Use parameter binding:

```js
await db.raw(
  `INSERT INTO secrets(owner_id, content) VALUES (?, ?)`,
  [userId, content]
);
```

Or use the query builder:

```js
await db('secrets').insert({
  owner_id: userId,
  content: content
});
```

Defense-in-depth:

- Restrict DB privileges by application path where feasible.
- Keep auth/session tables isolated from low-trust write flows.
- Add tests that insert payload-like strings and assert they remain data, not executable SQL.

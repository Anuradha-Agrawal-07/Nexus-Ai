# Nexus Core Database Design

## Overview

The database stores all persistent information required by Nexus Core.
Every future module (Gateway, Agents, Evaluation, Memory) will build upon
this database.

---

# Entity Relationship

User
│
├── owns ───────► Project
│                     │
│                     └── has ─────► API Key
│
└── creates ───► Audit Log

---

# Table 1 — Users

## Purpose

Stores all registered users of the Nexus platform.

Without this table:

- Nobody can log in.
- Projects cannot have owners.
- API keys cannot belong to anyone.

---

## Fields

| Field | Type | Description |
|---------|------|-------------|
| id | UUID | Unique identifier |
| username | String | User's display name |
| email | String | Login email |
| hashed_password | String | Encrypted password |
| role | Enum | admin / developer |
| is_active | Boolean | Whether account is active |
| created_at | Timestamp | Account creation time |
| updated_at | Timestamp | Last update time |

---

## Relationships

One User

↓

Many Projects

One User

↓

Many Audit Logs

---

# Table 2 — Projects

## Purpose

Represents an individual project created by a user.

In the future a project will contain:

- AI Models
- Workflows
- API Keys
- Agents
- Conversations

---

## Fields

| Field | Type | Description |
|---------|------|-------------|
| id | UUID | Project ID |
| owner_id | UUID | References User |
| name | String | Project name |
| description | Text | Project description |
| created_at | Timestamp | Creation date |
| updated_at | Timestamp | Last modification |

---

## Relationships

Many Projects

↓

Belong to one User

One Project

↓

Many API Keys

---

# Table 3 — API Keys

## Purpose

Allows external applications to authenticate with Nexus.

Future example

Frontend

↓

Authorization: Bearer nx_xxxxxxxxx

↓

Gateway

---

## Fields

| Field | Type | Description |
|---------|------|-------------|
| id | UUID | API Key ID |
| project_id | UUID | Parent project |
| key | String | Secret API key |
| status | Enum | active / revoked |
| last_used | Timestamp | Last request |
| expires_at | Timestamp | Expiration |
| created_at | Timestamp | Creation |

---

## Relationships

Many API Keys

↓

Belong to one Project

---

# Table 4 — Audit Logs

## Purpose

Stores important events happening in Nexus.

Examples

- User logged in
- Project created
- API key revoked

Useful for

- Monitoring
- Security
- Debugging

---

## Fields

| Field | Type | Description |
|---------|------|-------------|
| id | UUID | Log ID |
| user_id | UUID | User performing action |
| action | String | Action performed |
| resource | String | Object type |
| resource_id | UUID | Object ID |
| ip_address | String | Request IP |
| created_at | Timestamp | Time of action |

---

# Future Expansion

These tables will later connect to

- LLM Providers
- Agent Runs
- Conversations
- Workflows
- Evaluations
- Memory
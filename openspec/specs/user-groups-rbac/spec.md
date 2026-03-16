## Requirements

### Requirement: Group data model
The system SHALL maintain a `groups` table with columns: `id` (UUID PK), `name` (unique, not null), `description` (nullable), `created_at` (timestamp). A `user_groups` join table SHALL associate users and groups (composite PK: `user_id`, `group_id`).

#### Scenario: Create group
- **WHEN** an admin calls `POST /groups` with a unique `name`
- **THEN** the system SHALL create the group and return HTTP 201 with `group_id` and `name`

#### Scenario: Duplicate group name
- **WHEN** `POST /groups` is called with an already-existing `name`
- **THEN** the system SHALL return HTTP 409

### Requirement: Group CRUD API
The system SHALL provide group management endpoints accessible only to users in the `admin` group:
- `GET /groups` — list all groups
- `POST /groups` — create a group
- `GET /groups/{group_id}` — get group details with member list
- `DELETE /groups/{group_id}` — delete a group (removes all memberships)

#### Scenario: List groups as admin
- **WHEN** an authenticated admin calls `GET /groups`
- **THEN** the system SHALL return HTTP 200 with an array of group objects

#### Scenario: Access groups as non-admin
- **WHEN** an authenticated non-admin user calls `POST /groups`
- **THEN** the system SHALL return HTTP 403

### Requirement: User group membership management
The system SHALL provide endpoints for managing user-group memberships, accessible only to admin users:
- `POST /groups/{group_id}/members` — add a user to a group (body: `{"user_id": "<uuid>"}`)
- `DELETE /groups/{group_id}/members/{user_id}` — remove a user from a group

#### Scenario: Add user to group
- **WHEN** an admin calls `POST /groups/{group_id}/members` with a valid `user_id`
- **THEN** the system SHALL add the membership and return HTTP 200

#### Scenario: Add non-existent user
- **WHEN** `POST /groups/{group_id}/members` is called with a non-existent `user_id`
- **THEN** the system SHALL return HTTP 404

#### Scenario: Duplicate membership
- **WHEN** a user is already in a group and `POST /groups/{group_id}/members` is called again
- **THEN** the system SHALL return HTTP 409

### Requirement: Groups included in authenticated user context
The system SHALL include a `groups` field (list of group names) in the resolved `UserInfo` returned by `require_auth`. This allows route handlers to perform group-based authorization checks.

#### Scenario: Authenticated user with groups
- **WHEN** a user belonging to groups `["admin", "editors"]` makes an authenticated request
- **THEN** `require_auth` SHALL return `UserInfo` with `groups=["admin", "editors"]`

#### Scenario: Authenticated user with no groups
- **WHEN** a user belonging to no groups makes an authenticated request
- **THEN** `require_auth` SHALL return `UserInfo` with `groups=[]`

### Requirement: Admin group bootstrap
The system SHALL automatically create an `admin` group on startup if it does not exist. The first registered local user SHALL be automatically added to the `admin` group.

#### Scenario: First user registration gets admin
- **WHEN** `POST /auth/register` is called and no local users exist yet
- **THEN** the newly created user SHALL be added to the `admin` group

#### Scenario: Subsequent users do not get admin
- **WHEN** `POST /auth/register` is called and at least one local user already exists
- **THEN** the new user SHALL NOT be added to the `admin` group automatically
